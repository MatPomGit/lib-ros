from lib_ros import RosClient, MockBackend, ActionResult

backend = MockBackend(
    {"/demo": "std_msgs/msg/String"},
    services={"/add": ("example_interfaces/srv/AddTwoInts", sum)},
    actions={"/demo_action": lambda n: ActionResult(4, n + 1)},
)
with RosClient(backend=backend, allow_writes=True) as ros:
    with ros.subscribe("/demo", print):
        ros.publish("/demo", "synthetic")
        ros.spin_once(0)
    print(ros.call("/add", [2, 3], service_type="example_interfaces/srv/AddTwoInts"))
    print(ros.clock())
    print(ros.health())
