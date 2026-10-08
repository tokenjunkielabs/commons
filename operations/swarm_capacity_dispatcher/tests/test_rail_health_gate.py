import unittest

from operations.swarm_capacity_dispatcher.dispatcher import ContractError, dispatch, verify_receipt


WORKERS = [
    {
        "id": "builder",
        "capabilities": ["coding"],
        "capacity": 2,
        "token_budget": 20,
    }
]


def rail_health(*, cooldown=False, remaining=None, reset_at=None, domain="github-app"):
    return {
        "decision": "RAIL_HEALTH",
        "observed_at": "2026-10-06T18:30:00Z",
        "rails": [
            {
                "quota_domain": domain,
                "cooldown_active": cooldown,
                "request_budget_known": remaining is not None,
                "request_budget_remaining": remaining,
                "reset_at": reset_at,
            }
        ],
    }


def order(domain="github-app"):
    return {
        "id": "publish",
        "required_capabilities": ["coding"],
        "required_quota_domains": [domain],
        "token_cost": 1,
    }


class RailHealthGateTests(unittest.TestCase):
    def test_active_cooldown_defers_only_bound_work(self):
        result = dispatch(WORKERS, [order()], [], rail_health(cooldown=True))
        self.assertEqual(result["assignments"], [])
        self.assertEqual(
            result["unassigned"],
            [
                {
                    "order_id": "publish",
                    "reason": "RAIL_UNAVAILABLE",
                    "quota_domains": ["github-app"],
                }
            ],
        )

    def test_zero_request_budget_blocks_until_reset_but_not_after(self):
        blocked = dispatch(
            WORKERS,
            [order()],
            [],
            rail_health(remaining=0, reset_at="2026-10-06T18:31:00Z"),
        )
        self.assertEqual(blocked["unassigned"][0]["reason"], "RAIL_UNAVAILABLE")

        recovered = dispatch(
            WORKERS,
            [order()],
            [],
            rail_health(remaining=0, reset_at="2026-10-06T18:29:59Z"),
        )
        self.assertEqual([row["order_id"] for row in recovered["assignments"]], ["publish"])

    def test_unknown_domain_does_not_freeze_capacity(self):
        result = dispatch(
            WORKERS,
            [order("github-contributor")],
            [],
            rail_health(cooldown=True, domain="github-app"),
        )
        self.assertEqual([row["order_id"] for row in result["assignments"]], ["publish"])

    def test_receipt_is_bound_to_the_health_snapshot(self):
        blocked_health = rail_health(cooldown=True)
        receipt = dispatch(WORKERS, [order()], [], blocked_health)
        self.assertTrue(verify_receipt(WORKERS, [order()], [], receipt, blocked_health))
        self.assertFalse(
            verify_receipt(WORKERS, [order()], [], receipt, rail_health(cooldown=False))
        )

    def test_malformed_health_is_rejected(self):
        bad = rail_health()
        bad["rails"][0]["cooldown_active"] = "yes"
        with self.assertRaises(ContractError):
            dispatch(WORKERS, [order()], [], bad)


if __name__ == "__main__":
    unittest.main()
