"""Run with python examples/mock_read.py after installing the package."""
from lib_ros import MockBackend, RosClient

backend = MockBackend({"/demo": "std_msgs/msg/String"})
with RosClient(backend=backend) as ros:
    print(ros.topics())
    with ros.subscribe("/demo", print):
        backend.emit("/demo", "hello")
        ros.spin_once(0)
