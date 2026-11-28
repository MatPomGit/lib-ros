"""Read a ROS 2 topic from an already sourced ROS environment."""
import argparse
from lib_ros import RosClient

parser = argparse.ArgumentParser()
parser.add_argument("topic")
parser.add_argument("--type", required=True, dest="message_type")
parser.add_argument("--qos", choices=("default", "sensor_data"), default="default")
args = parser.parse_args()
with RosClient() as ros:
    print(ros.read(args.topic, message_type=args.message_type,
                   qos=10 if args.qos == "default" else args.qos))
