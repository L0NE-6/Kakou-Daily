import importlib.util
import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("kakou_daily", ROOT / "kakou_daily.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class FakeResponse:
    def __init__(self, payload, status=200, text=None):
        self.status_code = status
        self.text = text if text is not None else json.dumps(payload)


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.headers = {}
        self.proxies = {}
        self.calls = []
        self.closed = False

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        return self.response

    def close(self):
        self.closed = True


class FakeTransport:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.sessions = []

    def __call__(self):
        if not self.responses:
            raise AssertionError("unexpected HTTP request")
        session = FakeSession(self.responses.pop(0))
        self.sessions.append(session)
        return session


class AccountParsingTests(unittest.TestCase):
    def test_plain_accounts_and_duplicate_removal(self):
        accounts = MODULE.parse_accounts("主号|jwt-one\n副号|jwt-two\n重复|jwt-one")
        self.assertEqual([item.name for item in accounts], ["主号", "副号"])
        self.assertEqual([item.token for item in accounts], ["jwt-one", "jwt-two"])

    def test_json_accounts(self):
        accounts = MODULE.parse_accounts(
            json.dumps([{"name": "json", "token": "jwt-json"}])
        )
        self.assertEqual(accounts[0].name, "json")
        self.assertEqual(accounts[0].token, "jwt-json")

    def test_bearer_prefix_is_removed(self):
        accounts = MODULE.parse_accounts("Bearer jwt-one")
        self.assertEqual(accounts[0].token, "jwt-one")

    def test_only_ranges(self):
        self.assertEqual(MODULE.parse_only("1,3-4", 5), {1, 3, 4})


class FlowTests(unittest.TestCase):
    def account(self):
        return MODULE.Account("测试", "jwt-secret")

    def client(self, *responses):
        transport = FakeTransport(*responses)
        client = MODULE.KakouClient(
            api_base="https://kakou.example/api/v1",
            wait_seconds=0,
            session_factory=transport,
        )
        return client, transport

    def test_query_only_reads_profile_without_post(self):
        client, transport = self.client(
            FakeResponse({"data": {"balance": 10, "username": "u"}})
        )
        result = MODULE.run_account(1, self.account(), client, query_only=True)
        self.assertEqual(result.status, "QUERY")
        self.assertEqual(len(transport.sessions), 1)
        self.assertEqual(transport.sessions[0].calls[0][0], "GET")

    def test_claim_requires_positive_balance_delta(self):
        client, transport = self.client(
            FakeResponse({"data": {"balance": 10, "username": "u"}}),
            FakeResponse(
                {
                    "code": "claimed_success",
                    "amount": 5,
                    "next_checkin_at": "2026-11-25T00:00:00+08:00",
                }
            ),
            FakeResponse({"data": {"balance": 15, "username": "u"}}),
        )
        result = MODULE.run_account(1, self.account(), client)
        self.assertEqual(result.status, "CLAIMED")
        self.assertEqual(result.balance_delta, Decimal("5"))
        self.assertEqual(result.amount, Decimal("5"))
        self.assertEqual(len(transport.sessions), 3)
        post_headers = transport.sessions[1].calls[0][2]["headers"]
        self.assertEqual(post_headers["Content-Type"], "application/json")

    def test_claim_without_balance_growth_is_unconfirmed(self):
        client, _ = self.client(
            FakeResponse({"data": {"balance": 10}}),
            FakeResponse({"code": "claimed_success", "amount": 5}),
            FakeResponse({"data": {"balance": 10}}),
        )
        result = MODULE.run_account(1, self.account(), client)
        self.assertEqual(result.status, "UNCONFIRMED")
        self.assertIn("余额未增加", result.message)

    def test_already_claimed_is_neutral_success(self):
        client, _ = self.client(
            FakeResponse({"data": {"balance": 10}}),
            FakeResponse({"code": "CHECKIN_USER_ALREADY_CLAIMED"}),
            FakeResponse({"data": {"balance": 10}}),
        )
        result = MODULE.run_account(1, self.account(), client)
        self.assertEqual(result.status, "ALREADY")
        self.assertTrue(result.ok)

    def test_rate_limited_is_failure(self):
        client, _ = self.client(
            FakeResponse({"data": {"balance": 10}}),
            FakeResponse(
                {
                    "code": "CHECKIN_RATE_LIMITED",
                    "retry_after_seconds": 30,
                }
            ),
        )
        result = MODULE.run_account(1, self.account(), client)
        self.assertEqual(result.status, "RATE_LIMITED")
        self.assertFalse(result.ok)
        self.assertIn("30", result.message)

    def test_auth_error_is_visible(self):
        client, _ = self.client(FakeResponse({}, status=401))
        result = MODULE.run_account(1, self.account(), client)
        self.assertEqual(result.status, "AUTH_EXPIRED")
        self.assertFalse(result.ok)

    def test_unknown_claim_code_is_invalid_response(self):
        client, _ = self.client(
            FakeResponse({"data": {"balance": 10}}),
            FakeResponse({"code": "SOMETHING_NEW"}),
        )
        result = MODULE.run_account(1, self.account(), client)
        self.assertEqual(result.status, "INVALID_RESPONSE")
        self.assertFalse(result.ok)

    def test_summary_is_false_for_empty_or_failed_results(self):
        self.assertFalse(MODULE.build_summary([])["ok"])
        failed = MODULE.RunResult(1, "x", "API_ERROR", "boom")
        self.assertFalse(MODULE.build_summary([failed])["ok"])


if __name__ == "__main__":
    unittest.main()
