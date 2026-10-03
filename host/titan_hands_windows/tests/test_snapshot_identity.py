from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import unittest

from host.titan_hands_windows.protocol import DeltaTracker, ProtocolError


class SnapshotIdentityTests(unittest.TestCase):
    """Exercise production traversal without loading the native input backend."""

    @classmethod
    def setUpClass(cls):
        powershell = shutil.which("powershell") or shutil.which("pwsh")
        if powershell is None:
            raise unittest.SkipTest("PowerShell is unavailable")
        tests_dir = Path(__file__).resolve().parent
        fixture = str(tests_dir / "snapshot_identity_fixture.ps1").replace("'", "''")
        backend = str(tests_dir.parent / "backend.ps1").replace("'", "''")
        # Execute owned fixture text without changing machine execution policy.
        command = (
            f"& ([scriptblock]::Create([IO.File]::ReadAllText('{fixture}'))) "
            f"-BackendPath '{backend}'"
        )
        result = subprocess.run(
            [
                powershell,
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                command,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=60,
            check=False,
        )
        if result.returncode:
            raise AssertionError(
                f"snapshot fixture failed ({result.returncode}):\n"
                f"{result.stdout}\n{result.stderr}"
            )
        cls.cases = json.loads(result.stdout)

    def nodes_by_tag(self, case):
        return {node["tag"]: node for node in case["snapshot"]["nodes"]}

    def assert_unique_and_mapped(self, case):
        nodes = case["snapshot"]["nodes"]
        self.assertEqual(len(nodes), len({node["id"] for node in nodes}))
        for node in nodes:
            self.assertEqual(case["lookups"][node["id"]], node["tag"])

    def test_repeated_runtime_identity_keeps_first_mapping_and_subtree(self):
        case = self.cases["strong_duplicate"]
        self.assert_unique_and_mapped(case)
        nodes = self.nodes_by_tag(case)
        self.assertEqual(set(nodes), {"parent_a", "parent_b", "shared_a", "leaf_a"})
        self.assertEqual(nodes["shared_a"]["parent"], nodes["parent_a"]["id"])
        self.assertEqual(nodes["leaf_a"]["parent"], nodes["shared_a"]["id"])
        self.assertEqual(case["node_calls"].get("shared_a"), 1)
        self.assertNotIn("shared_b", case["node_calls"])
        self.assertEqual(case["first_child_calls"].get("shared_a"), 1)
        self.assertNotIn("shared_b", case["first_child_calls"])

    def test_identical_weak_siblings_remain_distinct(self):
        case = self.cases["weak_siblings"]
        self.assert_unique_and_mapped(case)
        nodes = self.nodes_by_tag(case)
        self.assertEqual(set(nodes), {"parent", "weak_a", "weak_b"})
        self.assertNotEqual(nodes["weak_a"]["id"], nodes["weak_b"]["id"])
        self.assertEqual(nodes["weak_a"]["name"], nodes["weak_b"]["name"])

    def test_weak_paths_include_the_parent_path(self):
        case = self.cases["weak_parent_paths"]
        self.assert_unique_and_mapped(case)
        nodes = self.nodes_by_tag(case)
        self.assertNotEqual(nodes["weak_a"]["id"], nodes["weak_b"]["id"])
        self.assertEqual(nodes["weak_a"]["parent"], nodes["parent_a"]["id"])
        self.assertEqual(nodes["weak_b"]["parent"], nodes["parent_b"]["id"])

    def test_handle_without_runtime_identity_does_not_merge_controls(self):
        case = self.cases["handle_only_collision"]
        self.assert_unique_and_mapped(case)
        nodes = self.nodes_by_tag(case)
        self.assertEqual(set(nodes), {"parent", "weak_a", "weak_b"})
        self.assertNotEqual(nodes["weak_a"]["id"], nodes["weak_b"]["id"])

    def test_filtering_preserves_original_sibling_numbering(self):
        hidden = self.cases["filter_hidden"]
        included = self.cases["filter_included"]
        self.assert_unique_and_mapped(hidden)
        self.assert_unique_and_mapped(included)
        hidden_nodes = self.nodes_by_tag(hidden)
        included_nodes = self.nodes_by_tag(included)
        self.assertNotIn("offscreen", hidden_nodes)
        self.assertIn("offscreen", included_nodes)
        self.assertEqual(hidden_nodes["visible"]["id"], included_nodes["visible"]["id"])

    def test_focused_weak_reference_uses_its_assigned_id(self):
        case = self.cases["weak_focus_reference"]
        self.assert_unique_and_mapped(case)
        nodes = self.nodes_by_tag(case)
        self.assertEqual(case["snapshot"]["focus_id"], nodes["weak_b"]["id"])
        self.assertEqual(case["lookups"][case["snapshot"]["focus_id"]], "weak_b")

    def test_focused_state_uses_its_assigned_id(self):
        case = self.cases["weak_focus_state"]
        nodes = self.nodes_by_tag(case)
        self.assertEqual(case["snapshot"]["focus_id"], nodes["weak_b"]["id"])

    def test_omitted_focused_element_does_not_return_an_unassigned_id(self):
        case = self.cases["omitted_focus"]
        self.assertNotIn("weak_b", self.nodes_by_tag(case))
        self.assertEqual(case["snapshot"]["focus_id"], "")
        self.assertTrue(case["snapshot"]["truncated"])

    def test_runtime_identity_retains_the_existing_hash(self):
        expected = "w_" + hashlib.sha256(b"7|42.777|456|menu").hexdigest()[:20]
        case = self.cases["strong_hash"]
        self.assertEqual(case["first"]["id"], expected)
        self.assertEqual(case["second"]["id"], expected)

    def test_identity_getters_are_read_once_per_queued_occurrence(self):
        case = self.cases["getter_once"]
        self.assert_unique_and_mapped(case)
        self.assertEqual(
            case["identity_reads"]["weak"],
            {"process_id": 1, "runtime_id": 1, "native_handle": 1, "automation_id": 1},
        )

    def test_same_element_sibling_cycle_terminates_before_requeue(self):
        case = self.cases["sibling_cycle"]
        self.assert_unique_and_mapped(case)
        self.assertEqual(set(self.nodes_by_tag(case)), {"parent", "weak_a", "weak_b"})
        self.assertLessEqual(case["sibling_calls"], 4)
        self.assertTrue(case["snapshot"]["truncated"])
        self.assertTrue(case["snapshot"]["coverage"]["sibling_cycle"])


class SnapshotValidationTests(unittest.TestCase):
    def test_duplicate_rejection_preserves_tracker_sequence_and_state(self):
        tracker = DeltaTracker()
        first = tracker.observe({"nodes": [{"id": "kept", "name": "Original"}]})
        with self.assertRaisesRegex(ProtocolError, "duplicate node id: collision"):
            tracker.observe({"nodes": [{"id": "collision"}, {"id": "collision"}]})
        self.assertEqual(tracker.sequence, first["sequence"])
        second = tracker.observe({"nodes": [{"id": "kept", "name": "Original"}]})
        self.assertEqual(second["base_sequence"], first["sequence"])
        self.assertEqual(second["added"], [])
        self.assertEqual(second["updated"], [])
        self.assertEqual(second["removed"], [])
        self.assertEqual(second["unchanged"], 1)


if __name__ == "__main__":
    unittest.main()
