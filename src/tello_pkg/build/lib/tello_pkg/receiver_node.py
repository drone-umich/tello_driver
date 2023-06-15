#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int64
from djitellopy import Tello
from rclpy.executors import MultiThreadedExecutor

class ReceiverNode(Node):
    def __init__(self):
        super().__init__("receiver_node")

        # Drone IP should be passed as a parameter
        drone_ip = self.declare_parameter("drone_ip").value

        # Connect to drone
        self.tello = Tello(drone_ip)
        self.tello.connect()

        # Subscriber
        self.subscription = self.create_subscription(String, "drone_command", self.command_callback, 10)

        # Publisher
        self.publisher_ = self.create_publisher(String, "drone_telemetry", 10)

        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.publish_telemetry)

    def publish_telemetry(self):
        msg = String()
        msg.data = f"Height: {str(self.tello.get_height())}, Battery: {str(self.tello.get_battery())}, Distance TOF: {str(self.tello.get_distance_tof())}\n Pitch: {str(self.tello.get_pitch())}, Roll: {str(self.tello.get_roll())}, Yaw: {str(self.tello.get_yaw())}"
        self.publisher_.publish(msg)



    def command_callback(self, msg):
        command = msg.data
        self.get_logger().info(f"Received command: {command}")

        if command == "connect":
            self.tello.connect()

        elif command == "takeoff":
            self.tello.takeoff()

        elif command == "flip_back":
            self.tello.flip_back()

        elif command == "flip_right":
            self.tello.flip_right()
            
        elif command.startswith("move_down"):
            _, distance = command.split()
            self.tello.move_down(int(distance))

        elif command.startswith("move_up"):
            _, distance = command.split()
            self.tello.move_up(int(distance))

        elif command.startswith("move_forward"):
            _, distance = command.split()
            self.tello.move_forward(int(distance))

        elif command.startswith("move_right"):
            _, distance = command.split()
            self.tello.move_right(int(distance))

        elif command.startswith("move_left"):
            _, distance = command.split()
            self.tello.move_left(int(distance))

        elif command.startswith("rotate_clockwise"):
            _, angle = command.split()
            self.tello.rotate_clockwise(int(angle))
        
        elif command.startswith("rotate_counter_clockwise"):
            _, angle = command.split()
            self.tello.rotate_counter_clockwise(int(angle))

        elif command == "get_height":
            print("Height: "+ str(self.tello.get_height()))

        elif command == "get_distance_tof":
            print("Distance TOF: "+ str(self.tello.get_distance_tof()))

        elif command == "get_battery":
            print("Battery: "+ str(self.tello.get_battery()))
        
        elif command == "get_speed_x":
            print("Speed X: "+ str(self.tello.get_speed_x()))

        elif command == "get_speed_y":
            print("Speed Y: "+ str(self.tello.get_speed_y()))

        elif command == "land":
            self.tello.land()


def main(args=None):
    rclpy.init(args=args)
    node = ReceiverNode() 

    executor = MultiThreadedExecutor(num_threads=2) # You can adjust the number of threads

    executor.add_node(node)

    try:
        executor.spin()  # This will block until the node is ready to be shut down
    except KeyboardInterrupt:
        pass

    executor.shutdown()


if __name__ == "__main__":
    main()
