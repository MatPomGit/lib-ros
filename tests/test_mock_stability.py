"""Regression tests for fair mock dispatch and synchronous timeout semantics."""
import unittest
from unittest.mock import patch

from lib_ros import ActionResult, MockBackend, RosClient, RosTimeout


class MockStabilityTests(unittest.TestCase):
    def test_busy_queue_does_not_starve_other_subscriptions(self):
        backend = MockBackend({"/fast": "type", "/slow": "type"})
        received = []
        with RosClient(backend=backend) as ros:
            with ros.subscribe("/fast", lambda m: received.append(("fast", m))):
                with ros.subscribe("/slow", lambda m: received.append(("slow", m))):
                    backend.emit("/fast", 1)
                    backend.emit("/fast", 2)
                    backend.emit("/slow", 3)
                    ros.spin_once(0)
                    backend.emit("/fast", 4)
                    ros.spin_once(0)
                    self.assertEqual(received, [("fast", 1), ("slow", 3)])
                ros.spin_once(0)
                self.assertEqual(received[-1], ("fast", 2))

    def test_late_service_and_action_results(self):
        invoked = []
        def handler(request):
            invoked.append(request)
            return ActionResult(4, request)

        backend = MockBackend(services={"/svc": ("type", handler)},
                              actions={"/act": handler})
        with RosClient(backend=backend, allow_writes=True) as ros:
            for operation in (
                lambda: ros.call("/svc", 1, service_type="type", timeout=1),
                lambda: ros.send_goal("/act", 2, action_type="type", timeout=1),
            ):
                with patch("lib_ros._mock.monotonic", side_effect=[10, 12]):
                    with self.assertRaises(RosTimeout):
                        operation()
            self.assertEqual(invoked, [1, 2])
            self.assertEqual(ros.health().timeouts, 2)

    def test_zero_timeout_does_not_invoke_handler(self):
        invoked = []
        backend = MockBackend(services={"/svc": ("type", invoked.append)},
                              actions={"/act": invoked.append})
        with RosClient(backend=backend, allow_writes=True) as ros:
            with self.assertRaises(RosTimeout):
                ros.call("/svc", 1, service_type="type", timeout=0)
            with self.assertRaises(RosTimeout):
                ros.send_goal("/act", 2, action_type="type", timeout=0)
            self.assertEqual(invoked, [])
            self.assertEqual(ros.health().timeouts, 2)


if __name__ == "__main__":
    unittest.main()
