"""Optional native ROS 2 backend; imported only when requested."""
from .models import TopicDescriptor, RosUnavailable


class NativeBackend:
    def __init__(self, node_name, namespace, domain_id):
        try:
            import rclpy
            from rclpy.context import Context
            from rclpy.executors import SingleThreadedExecutor
            from rclpy.qos import qos_profile_sensor_data
            from rosidl_runtime_py.utilities import get_message
        except ImportError as exc:
            raise RosUnavailable("source a compatible ROS 2 installation first") from exc
        self._rclpy = rclpy
        self._get_message = get_message
        self._sensor_qos = qos_profile_sensor_data
        self._context = Context()
        self._node = None
        self._executor = None
        try:
            rclpy.init(args=[], context=self._context, domain_id=domain_id)
            self._node = rclpy.create_node(
                node_name, namespace=namespace, context=self._context,
                use_global_arguments=False,
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

    def spin_once(self, timeout):
        self._executor.spin_once(timeout_sec=timeout)

    def close(self):
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
