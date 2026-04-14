import sys
import rclpy
from rclpy.node import Node

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

from geometry_msgs.msg import Twist


class TurtleController(Node):

    def __init__(self):
        super().__init__('qt_turtle_controller')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

    def move_forward(self):
        msg = Twist()
        msg.linear.x = 2.0
        self.publisher_.publish(msg)

    def turn(self):
        msg = Twist()
        msg.angular.z = 2.0
        self.publisher_.publish(msg)


class ControlWindow(QWidget):

    def __init__(self, ros_node):
        super().__init__()

        self.node = ros_node

        self.setWindowTitle("Control Tortuga")

        layout = QVBoxLayout()

        btn_forward = QPushButton("Avanzar")
        btn_forward.clicked.connect(self.node.move_forward)

        btn_turn = QPushButton("Girar")
        btn_turn.clicked.connect(self.node.turn)

        layout.addWidget(btn_forward)
        layout.addWidget(btn_turn)

        self.setLayout(layout)


def main():
    rclpy.init()

    node = TurtleController()

    app = QApplication(sys.argv)
    window = ControlWindow(node)
    window.show()

    # Timer ROS2 dentro de Qt loop
    timer = node.create_timer(0.1, lambda: None)

    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0)
            app.processEvents()
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()