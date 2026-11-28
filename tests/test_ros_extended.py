import unittest
from lib_ros import (RosClient, MockBackend, ActionResult, RosTimeout,
                     RosWriteDisabled, RosError)


class ExtendedTests(unittest.TestCase):
    def setUp(self):
        ticks = iter([100, 200, 50])
        self.backend = MockBackend(
            {"/out": "std_msgs/msg/String"},
            services={"/add": ("example_interfaces/srv/AddTwoInts", sum)},
            actions={"/demo": lambda value: ActionResult(4, value + 1)},
            transforms={("map", "base", None): "pose"},
            ros_clock=lambda: next(ticks),
        )

    def test_write_guard(self):
        with RosClient(backend=self.backend) as ros:
            for operation in (
                lambda: ros.publish("/out", "msg"),
                lambda: ros.call("/add", [1, 2], service_type="type"),
                lambda: ros.send_goal("/demo", 1, action_type="type"),
            ):
                with self.assertRaises(RosWriteDisabled):
                    operation()
            self.assertEqual(ros.health().messages_published, 0)

    def test_mock_roundtrip(self):
        with RosClient(backend=self.backend, allow_writes=True) as ros:
            messages = []
            with ros.subscribe("/out", messages.append, qos=1):
                ros.publish("/out", "a")
                ros.publish("/out", "b")
                ros.spin_once(0)
                self.assertEqual(messages, ["b"])
                health = ros.health()
                self.assertEqual((health.messages_received, health.messages_published,
                                  health.local_drops, health.subscriptions), (1, 2, 1, 1))
            self.assertEqual(ros.health().subscriptions, 0)
            self.assertEqual(ros.services()[0].name, "/add")
            self.assertEqual(ros.call("/add", [2, 3], service_type="type"), 5)
            self.assertEqual(ros.send_goal("/demo", 3, action_type="type"), ActionResult(4, 4))

    def test_clock_and_transform(self):
        with RosClient(backend=self.backend) as ros:
            a, b, c = ros.clock(), ros.clock(), ros.clock()
            self.assertTrue(a.simulated)
            self.assertEqual((a.ros_ns, b.ros_ns, c.ros_ns), (100, 200, 50))
            self.assertLessEqual(a.monotonic_ns, c.monotonic_ns)
            self.assertEqual(ros.health().clock_regressions, 1)
            self.assertEqual(ros.transform("map", "base"), "pose")
            with self.assertRaises(RosTimeout):
                ros.transform("map", "absent", timeout=0)
            self.assertEqual(ros.health().timeouts, 1)

    def test_callback_blocking_rejected(self):
        with RosClient(backend=self.backend, allow_writes=True) as ros:
            def callback(_):
                with self.assertRaises(RosError):
                    ros.call("/add", [1], service_type="type")
            with ros.subscribe("/out", callback):
                ros.publish("/out", "a")
                ros.spin_once(0)

    def test_missing_and_validation(self):
        with RosClient(backend=self.backend, allow_writes=True) as ros:
            with self.assertRaises(RosTimeout):
                ros.call("/missing", 1, service_type="type", timeout=0)
            with self.assertRaises(RosTimeout):
                ros.send_goal("/missing", 1, action_type="type", timeout=0)
            with self.assertRaises(ValueError):
                ros.transform("/map", "base")
            with self.assertRaises(ValueError):
                ros.transform("map", "base", stamp_ns=0)
            self.assertEqual(ros.health().timeouts, 2)


if __name__ == "__main__":
    unittest.main()
