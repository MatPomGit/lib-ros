"""Real ROS 2 DDS smoke test with synthetic String data, no hardware."""
from threading import Event, Thread
from time import monotonic

import rclpy
from rclpy.context import Context
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import String

from lib_ros import RosClient, RosTimeout, RosError


def main():
    domain = 77
    topic = "/lib_ros_ci/telemetry"
    missing = "/lib_ros_ci/no_publisher"
    context = Context()
    rclpy.init(args=[], context=context, domain_id=domain)
    node = None
    stop = Event()
    producer = None
    try:
        node = rclpy.create_node("lib_ros_ci_source", context=context)
        publisher = node.create_publisher(String, topic, qos_profile_sensor_data)

        def produce():
            while not stop.is_set():
                publisher.publish(String(data="lib-ros-ci"))
                stop.wait(0.05)

        producer = Thread(target=produce)
        producer.start()
        with RosClient(node_name="lib_ros_ci_client", domain_id=domain) as ros:
            deadline = monotonic() + 15
            while monotonic() < deadline:
                if any(t.name == topic and "std_msgs/msg/String" in t.types
                       for t in ros.topics()) and ("lib_ros_ci_source", "/") in ros.nodes():
                    break
                ros.spin_once(0.1)
            else:
                raise AssertionError("DDS graph did not discover publisher")
            message = ros.read(topic, timeout=10, qos="sensor_data")
            assert isinstance(message, String) and message.data == "lib-ros-ci"
            messages = []
            with ros.subscribe(topic, messages.append, message_type=String,
                               qos="sensor_data"):
                deadline = monotonic() + 10
                while not messages and monotonic() < deadline:
                    ros.spin_once(0.1)
                assert messages and messages[0].data == "lib-ros-ci"
            try:
                ros.read(missing, message_type=String, timeout=0.2)
            except RosTimeout:
                pass
            else:
                raise AssertionError("expected timeout without publisher")

            def close_on_message(message):
                assert message.data == "lib-ros-ci"
                ros.close()

            with ros.subscribe(topic, close_on_message, message_type=String,
                               qos="sensor_data"):
                deadline = monotonic() + 10
                while monotonic() < deadline:
                    try:
                        ros.spin_once(0.1)
                    except RosError:
                        break
                else:
                    raise AssertionError("callback did not close the client")
        assert context.ok(), "client must not shut down the publisher context"
    finally:
        stop.set()
        if producer is not None:
            producer.join()
        if node is not None:
            node.destroy_node()
        context.try_shutdown()
    print("PASS: native ROS 2 graph, typed read, subscription, QoS, timeout, callback cleanup")


if __name__ == "__main__":
    main()
