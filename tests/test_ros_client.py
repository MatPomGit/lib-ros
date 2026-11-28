"""Offline functional tests of the public client."""
import unittest
from threading import Thread
from time import monotonic
from lib_ros import MockBackend, RosClient, RosError, RosTimeout, RosUnavailable


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.backend = MockBackend({"/imu": "sensor_msgs/msg/Imu"},
                                   nodes=[("sensor", "/")])
        self.ros = RosClient(backend=self.backend)
        self.addCleanup(self.ros.close)

    def test_graph(self):
        self.assertEqual(self.ros.topics()[0].types, ("sensor_msgs/msg/Imu",))
        self.assertEqual(self.ros.nodes(), [("sensor", "/")])

    def test_subscription_and_cleanup(self):
        messages = []
        with self.ros.subscribe("/imu", messages.append):
            message = object()
            self.backend.emit("/imu", message)
            self.ros.spin_once(0)
            self.assertIs(messages[0], message)
        self.backend.emit("/imu", 2)
        self.ros.spin_once(0)
        self.assertEqual(len(messages), 1)

    def test_bounded_queue(self):
        messages = []
        with self.ros.subscribe("/imu", messages.append, qos=2):
            for value in range(5):
                self.backend.emit("/imu", value)
            self.ros.spin_once(0)
            self.ros.spin_once(0)
        self.assertEqual(messages, [3, 4])

    def test_read(self):
        # Repeat until the temporary subscription is created; no fixed startup delay.
        import threading
        stop = threading.Event()
        message = object()
        def produce():
            while not stop.is_set():
                self.backend.emit("/imu", message)
                stop.wait(0.005)
        thread = Thread(target=produce)
        thread.start()
        try:
            self.assertIs(self.ros.read("/imu", timeout=1), message)
        finally:
            stop.set()
            thread.join()

    def test_timeout_and_cancel(self):
        start = monotonic()
        with self.assertRaises(RosTimeout):
            self.ros.read("/imu", timeout=0.02)
        self.assertLess(monotonic() - start, 1)
        self.assertFalse(self.backend._subscriptions)

    def test_unknown_topic(self):
        with self.assertRaises(RosUnavailable):
            self.ros.subscribe("/missing", print)
        with self.ros.subscribe("/missing", print, message_type="std_msgs/msg/String"):
            pass

    def test_invalid_inputs(self):
        for timeout in (-1, float("inf"), float("nan"), True):
            with self.assertRaises(ValueError):
                self.ros.spin_once(timeout)
        for qos in (0, -1, True, "unknown"):
            with self.assertRaises(ValueError):
                self.ros.subscribe("/imu", print, qos=qos)
        with self.assertRaises(ValueError):
            self.ros.subscribe("relative", print)

    def test_closed(self):
        self.ros.close()
        self.ros.close()
        with self.assertRaises(RosError):
            self.ros.topics()
        with self.assertRaises(RosError):
            self.backend.emit("/imu", 1)

    def test_close_from_callback(self):
        def stop(_):
            self.ros.close()
        self.ros.subscribe("/imu", stop)
        self.backend.emit("/imu", 1)
        self.ros.spin()
        self.assertFalse(self.backend._subscriptions)
        with self.assertRaises(RosError):
            self.ros.topics()

    def test_nested_spin_and_read_rejected(self):
        def callback(_):
            with self.assertRaises(RosError):
                self.ros.spin_once(0)
            with self.assertRaises(RosError):
                self.ros.read("/imu")
        with self.ros.subscribe("/imu", callback):
            self.backend.emit("/imu", 1)
            self.ros.spin_once(0)

    def test_sensor_data_queue(self):
        messages = []
        with self.ros.subscribe("/imu", messages.append, qos="sensor_data"):
            for value in range(7):
                self.backend.emit("/imu", value)
            for _ in range(5):
                self.ros.spin_once(0)
        self.assertEqual(messages, [2, 3, 4, 5, 6])


if __name__ == "__main__":
    unittest.main()
