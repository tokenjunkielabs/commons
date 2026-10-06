import unittest

from qloo_adapter import QlooAdapterError, QlooClient


class RecordingTransport:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def __call__(self, url, headers, payload, timeout_seconds):
        self.calls.append((url, dict(headers), dict(payload), timeout_seconds))
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


class QlooClientTests(unittest.TestCase):
    def test_current_insights_contract_and_normalization(self):
        transport = RecordingTransport({
            "success": True,
            "duration": 37,
            "query": {"explainability": {"warning": "partial influence data"}},
            "results": {"entities": [{
                "entity_id": "place-1",
                "name": "Example Venue",
                "type": "urn:entity:place",
                "properties": {"geocode": {"city": "New York"}},
                "query": {"affinity": 0.87, "explainability": {"seed-brand": 0.74}},
            }]},
        })
        client = QlooClient("placeholder-not-a-secret", transport=transport)

        result = client.insights(
            filter_type="urn:entity:place",
            interest_entity_queries=["Jil Sander", "Brian Eno"],
            location_query="New York City",
            take=5,
        )

        self.assertEqual(result.state, "ok")
        self.assertEqual(result.entities[0].affinity, 0.87)
        self.assertEqual(result.entities[0].evidence, {"seed-brand": 0.74})
        url, headers, payload, timeout_seconds = transport.calls[0]
        self.assertEqual(url, "https://api.qloo.com/v2/insights")
        self.assertEqual(payload["signal.interests.entities.query"], ["Jil Sander", "Brian Eno"])
        self.assertEqual(payload["filter.location.query"], "New York City")
        self.assertTrue(payload["feature.explainability"])
        self.assertEqual(payload["take"], 5)
        self.assertEqual(timeout_seconds, 10.0)

    def test_empty_evidence_stays_empty(self):
        transport = RecordingTransport({"success": True, "results": {"entities": []}})
        result = QlooClient("placeholder-not-a-secret", transport=transport).insights(
            filter_type="urn:entity:brand",
            interest_tags=["urn:tag:genre:media:ambient"],
        )
        self.assertEqual(result.state, "empty")
        self.assertEqual(result.entities, ())
        self.assertEqual(transport.calls[0][2]["signal.interests.tags"], "urn:tag:genre:media:ambient")

    def test_invalid_inputs_fail_before_transport(self):
        transport = RecordingTransport({"success": True, "results": {"entities": []}})
        client = QlooClient("placeholder-not-a-secret", transport=transport)
        with self.assertRaises(QlooAdapterError):
            client.insights(filter_type="urn:entity:place", location_query="Chicago", take=51)
        with self.assertRaises(QlooAdapterError):
            client.insights(filter_type="urn:entity:place")
        self.assertEqual(transport.calls, [])

    def test_transport_error_is_structured(self):
        transport = RecordingTransport(TimeoutError("boom"))
        client = QlooClient("placeholder-not-a-secret", transport=transport)
        with self.assertRaises(QlooAdapterError) as raised:
            client.insights(filter_type="urn:entity:destination", interest_entity_ids=["seed-1"])
        self.assertEqual(raised.exception.code, "transport_error")


if __name__ == "__main__":
    unittest.main()
