"""Native ROS 2 round-trip with only synthetic interfaces."""
from threading import Event, Thread
from time import monotonic

import rclpy
from rclpy.context import Context
from rclpy.executors import SingleThreadedExecutor
from rclpy.action import ActionServer
from action_msgs.msg import GoalStatus
from example_interfaces.action import Fibonacci
from example_interfaces.srv import AddTwoInts
from geometry_msgs.msg import TransformStamped
from std_msgs.msg import String
from tf2_ros import StaticTransformBroadcaster

from lib_ros import RosClient, RosTimeout, RosWriteDisabled


def main():
    domain = 78
    context = Context()
    rclpy.init(args=[], context=context, domain_id=domain)
    node = rclpy.create_node("lib_ros_extended_source", context=context)
    executor = SingleThreadedExecutor(context=context)
    executor.add_node(node)
    stop = Event()
    received = Event()
    received_data = []

    def on_message(msg):
        received_data.append(msg.data)
        received.set()

    sub = node.create_subscription(String, "/lib_ros_ci/out", on_message, 10)

    def add(request, response):
        response.sum = request.a + request.b
        return response

    service = node.create_service(AddTwoInts, "/lib_ros_ci/add", add)

    def execute(handle):
        handle.succeed()
        return Fibonacci.Result(sequence=[0, 1, 1])

    action = ActionServer(node, Fibonacci, "/lib_ros_ci/fibonacci", execute)
    broadcaster = StaticTransformBroadcaster(node)
    transform = TransformStamped()
    transform.header.stamp = node.get_clock().now().to_msg()
    transform.header.frame_id = "map"
    transform.child_frame_id = "base"
    transform.transform.translation.x = 2.0
    transform.transform.rotation.w = 1.0
    broadcaster.sendTransform(transform)

    def spin_source():
        while not stop.is_set():
            executor.spin_once(timeout_sec=0.1)

    thread = Thread(target=spin_source)
    thread.start()
    try:
        with RosClient(domain_id=domain) as read_only:
            try:
                read_only.publish("/lib_ros_ci/out", String(data="blocked"))
            except RosWriteDisabled:
                pass
            else:
                raise AssertionError("write guard failed")
        with RosClient(domain_id=domain, allow_writes=True) as ros:
            deadline = monotonic() + 10
            while not received.is_set() and monotonic() < deadline:
                ros.publish("/lib_ros_ci/out", String(data="synthetic"))
                received.wait(0.1)
            assert received_data and received_data[0] == "synthetic"
            response = ros.call("/lib_ros_ci/add", AddTwoInts.Request(a=2, b=3),
                                service_type="example_interfaces/srv/AddTwoInts", timeout=10)
            assert response.sum == 5
            result = ros.send_goal("/lib_ros_ci/fibonacci", Fibonacci.Goal(order=3),
                                   action_type="example_interfaces/action/Fibonacci", timeout=10)
            assert result.status == GoalStatus.STATUS_SUCCEEDED
            assert list(result.result.sequence) == [0, 1, 1]
            pose = ros.transform("map", "base", timeout=10)
            assert pose.transform.translation.x == 2.0
            clock = ros.clock()
            assert clock.ros_ns > 0 and clock.monotonic_ns > 0 and not clock.simulated
            try:
                ros.call("/lib_ros_ci/absent", AddTwoInts.Request(),
                         service_type=AddTwoInts, timeout=0.2)
            except RosTimeout:
                pass
            else:
                raise AssertionError("missing service should time out")
            health = ros.health()
            assert health.ready and health.messages_published >= 1
            assert health.timeouts == 1 and health.local_drops is None
        assert context.ok()
    finally:
        stop.set()
        thread.join()
        action.destroy()
        executor.shutdown()
        node.destroy_node()
        context.try_shutdown()
    print("PASS: native publish, service, action, TF2, clocks, health and write guard")


if __name__ == "__main__":
    main()
