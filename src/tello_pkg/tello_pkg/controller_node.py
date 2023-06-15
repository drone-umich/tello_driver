#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int64
import time
from rclpy.executors import MultiThreadedExecutor
import asyncio

class ControllerNode(Node):
    def __init__(self):
        super().__init__("controller_node")

        # Time of last telemetry received
        self.last_telemetry_time = None

        # Publisher
        self.publisher_ = self.create_publisher(String, "drone_command", 10)

        # Subscriber
        self.subscription = self.create_subscription(String, "drone_telemetry", self.telemetry_callback, 10)

        self.send_commands()

        #Timer
        self.create_timer(0.5, self.telemetry_check)

    def send_commands(self):
        # Commands to be sent
        commands1 = [
            'connect',
            'takeoff',
            'move_up 50',
            'move_forward 50',
            'rotate_clockwise 90',
            'get_height',
            'move_forward 50',
            'rotate_clockwise 90',
            'get_distance_tof',
            'move_forward 50',
            'rotate_clockwise 90',
            'get_battery',
            'move_forward 50',
            'rotate_clockwise 90',
            'land'
        ]
        commands2 = [
            'connect',
            'takeoff',
            'move_forward 100',
            'move_right 100',
            'rotate_clockwise 90',
            'move_forward 50',
            'land'
        ]

        for command in commands2:
            msg = String()
            msg.data = command
            self.publisher_.publish(msg)
            self.get_logger().info(f"Command sent: {msg.data}")
            rclpy.spin_once(self, timeout_sec=0.5)
        
            # Wait for the command to be processed
            time.sleep(0.5)

    def telemetry_check(self):
        if self.last_telemetry_time is None or time.time() - self.last_telemetry_time > 0.5:
            self.get_logger().info("No telemetry received.")
        #else:
            #self.get_logger().info("Telemetry received.")
    
    def telemetry_callback(self, msg):
        self.get_logger().info(f"Telemetry: {msg.data}")
        self.last_telemetry_time = time.time()


def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode() 

    executor = MultiThreadedExecutor(num_threads=2) # You can adjust the number of threads

    executor.add_node(node)

    try:
        executor.spin()  # This will block until the node is ready to be shut down
    except KeyboardInterrupt:
        pass

    executor.shutdown()
    #rclpy.spin(node)

if __name__ == "__main__":
    main()
