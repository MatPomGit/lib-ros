"""Check the installed public package against the versioned source contract."""
import importlib.metadata
import inspect
import json
from pathlib import Path
import unittest

import lib_ros

ROOT = Path(__file__).resolve().parents[1]


class PublicApiTests(unittest.TestCase):
    def test_exact_exports_and_version(self):
        contract = json.loads((ROOT / "contracts/api.json").read_text())
        declared = {name.split(".")[-1] for name in contract["public_entrypoints"]}
        self.assertEqual(declared, set(lib_ros.__all__))
        for name in declared:
            self.assertTrue(hasattr(lib_ros, name), name)
        self.assertEqual(importlib.metadata.version("lib-ros"), contract["api_version"])

    def test_client_methods(self):
        methods = {
            "topics", "nodes", "services", "subscribe", "read", "spin",
            "spin_once", "close", "publish", "call", "send_goal",
            "transform", "clock", "health",
        }
        self.assertEqual(methods, {name for name, value in inspect.getmembers(
            lib_ros.RosClient, inspect.isfunction) if not name.startswith("_")})
        sig = inspect.signature(lib_ros.RosClient)
        self.assertIs(sig.parameters["allow_writes"].default, False)
        self.assertIs(sig.parameters["use_sim_time"].default, False)
        self.assertIsNone(sig.parameters["backend"].default)


if __name__ == "__main__":
    unittest.main()
