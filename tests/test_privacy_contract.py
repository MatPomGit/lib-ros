"""Static regression checks for privacy gates in the proposed ROS2 contract.

No ROS runtime, network access, or device is started by these tests.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate_privacy_policy(policy: str, manifest: dict) -> list[str]:
    required = {
        "classification": "Klasy danych i granice zaufania",
        "egress": "Zasada odmowy dostępu i transmisji",
        "default_deny": "DENY",
        "retention": "retencji",
        "negative_tests": "testy negatywne",
        "not_implemented": "NOT_IMPLEMENTED",
        "not_run": "NOT_RUN",
    }
    errors = [name for name, marker in required.items() if marker not in policy]
    if not isinstance(manifest, dict):
        return errors + ["invalid manifest"]
    missing = [key for key in ("data_classification", "network_egress") if key not in manifest]
    if missing and not all(key in policy for key in missing):
        errors.append("undeclared deferred manifest controls")
    return errors


class PrivacyContractTests(unittest.TestCase):
    def setUp(self):
        self.policy = (ROOT / "docs/privacy.md").read_text(encoding="utf-8")
        self.manifest = json.loads(
            (ROOT / "config/component.json").read_text(encoding="utf-8")
        )

    def test_current_proposed_policy_is_explicit(self):
        self.assertEqual([], validate_privacy_policy(self.policy, self.manifest))

    def test_missing_default_deny_is_detected(self):
        changed = self.policy.replace("DENY", "ALLOW")
        self.assertIn("default_deny", validate_privacy_policy(changed, self.manifest))

    def test_missing_egress_contract_is_detected(self):
        changed = self.policy.replace(
            "Zasada odmowy dostępu i transmisji", "Transport"
        )
        self.assertIn("egress", validate_privacy_policy(changed, self.manifest))

    def test_missing_manifest_field_disclosure_is_detected(self):
        changed = self.policy.replace("network_egress", "outbound_rules")
        self.assertIn(
            "undeclared deferred manifest controls",
            validate_privacy_policy(changed, self.manifest),
        )


if __name__ == "__main__":
    unittest.main()
