"""Optional native ROS 2 backend; imported only when requested."""
from time import monotonic, monotonic_ns, time_ns
from .models import (TopicDescriptor, RosUnavailable, RosError, RosTimeout,
                     ClockSnapshot, ActionResult)


class NativeBackend:
    name = 'native'
    local_drops = None

    def __init__(self, node_name, namespace, domain_id, use_sim_time=False):
        try:
            import rclpy
            from rclpy.context import Context
            from rclpy.executors import SingleThreadedExecutor
            from rclpy.qos import qos_profile_sensor_data
            from rclpy.parameter import Parameter
            from rosidl_runtime_py.utilities import get_message
        except ImportError as exc:
            raise RosUnavailable("source a compatible ROS 2 installation first") from exc
        self._rclpy = rclpy
        self._get_message = get_message
        self._sensor_qos = qos_profile_sensor_data
        self._context = Context()
        self._node = None
        self._executor = None
        self._publishers = {}
        self._tf_listener = None
        self._tf_buffer = None
        try:
            rclpy.init(args=[], context=self._context, domain_id=domain_id)
            self._node = rclpy.create_node(
                node_name, namespace=namespace, context=self._context,
                use_global_arguments=False,
                parameter_overrides=[Parameter('use_sim_time', value=use_sim_time)],
            )
            self._executor = SingleThreadedExecutor(context=self._context)
            self._executor.add_node(self._node)
        except BaseException:
            self.close()
            raise

    def topics(self):
        return [TopicDescriptor(name, tuple(sorted(types)))
                for name, types in sorted(self._node.get_topic_names_and_types())]

    def nodes(self):
        return sorted(self._node.get_node_names_and_namespaces())

    def subscribe(self, topic, callback, message_type, qos):
        if message_type is None:
            types = next((t.types for t in self.topics() if t.name == topic), ())
            if len(types) != 1:
                raise RosUnavailable(f"topic {topic} not discovered or ambiguous; specify message_type")
            message_type = types[0]
        if isinstance(message_type, str):
            try:
                message_type = self._get_message(message_type)
            except (ImportError, AttributeError, ValueError) as exc:
                raise RosUnavailable(f"message type unavailable: {message_type}") from exc
        profile = self._sensor_qos if qos == "sensor_data" else qos
        subscription = self._node.create_subscription(message_type, topic, callback, profile)
        return lambda: self._node.destroy_subscription(subscription)

    def ready(self):
        return self._context.ok()

    def publish(self, topic, message, qos):
        key = (topic, type(message), qos)
        publisher = self._publishers.get(key)
        if publisher is None:
            profile = self._sensor_qos if qos == "sensor_data" else qos
            publisher = self._node.create_publisher(type(message), topic, profile)
            self._publishers[key] = publisher
        publisher.publish(message)

    def services(self):
        return [TopicDescriptor(name, tuple(sorted(types)))
                for name, types in sorted(self._node.get_service_names_and_types())]

    def _resolve(self, kind, value):
        if not isinstance(value, str):
            return value
        from rosidl_runtime_py.utilities import get_service, get_action
        try:
            return (get_service if kind == "service" else get_action)(value)
        except (ImportError, AttributeError, ValueError) as exc:
            raise RosUnavailable(f"{kind} type unavailable: {value}") from exc

    def _remaining(self, deadline):
        remaining = deadline - monotonic()
        if remaining <= 0:
            raise RosTimeout("ROS operation timed out; remote execution may continue")
        return remaining

    def _wait(self, future, deadline):
        while not future.done():
            self.spin_once(min(0.1, self._remaining(deadline)))
        return future.result()

    def call(self, name, request, service_type, timeout):
        deadline = monotonic() + timeout
        client = self._node.create_client(self._resolve("service", service_type), name)
        try:
            if not client.wait_for_service(timeout_sec=self._remaining(deadline)):
                raise RosTimeout(f"service unavailable: {name}")
            return self._wait(client.call_async(request), deadline)
        finally:
            self._node.destroy_client(client)

    def send_goal(self, name, goal, action_type, timeout):
        from rclpy.action import ActionClient
        deadline = monotonic() + timeout
        client = ActionClient(self._node, self._resolve("action", action_type), name)
        try:
            if not client.wait_for_server(timeout_sec=self._remaining(deadline)):
                raise RosTimeout(f"action unavailable: {name}")
            handle = self._wait(client.send_goal_async(goal), deadline)
            if not handle.accepted:
                raise RosError(f"action goal rejected: {name}")
            response = self._wait(handle.get_result_async(), deadline)
            return ActionResult(response.status, response.result)
        finally:
            client.destroy()

    def transform(self, target, source, stamp_ns, timeout):
        try:
            from tf2_ros import Buffer, TransformListener, TransformException
            from rclpy.time import Time
        except ImportError as exc:
            raise RosUnavailable("tf2_ros is required for transforms") from exc
        deadline = monotonic() + timeout
        if self._tf_listener is None:
            self._tf_buffer = Buffer(node=self._node)
            self._tf_listener = TransformListener(self._tf_buffer, self._node,
                                                  spin_thread=False)
        stamp = Time(nanoseconds=stamp_ns or 0, clock_type=self._node.get_clock().clock_type)
        while True:
            try:
                return self._tf_buffer.lookup_transform(target, source, stamp)
            except TransformException:
                self.spin_once(min(0.1, self._remaining(deadline)))

    def clock(self):
        return ClockSnapshot(self._node.get_clock().now().nanoseconds,
                             time_ns(), monotonic_ns(),
                             bool(self._node.get_parameter("use_sim_time").value))

    def spin_once(self, timeout):
        self._executor.spin_once(timeout_sec=timeout)

    def close(self):
        try:
            if self._tf_listener is not None:
                self._tf_listener.unregister()
        finally:
            self._close_context()

    def _close_context(self):
        try:
            if self._executor is not None:
                self._executor.shutdown()
        finally:
            try:
                if self._node is not None:
                    self._node.destroy_node()
            finally:
                if self._context.ok():
                    self._context.try_shutdown()
