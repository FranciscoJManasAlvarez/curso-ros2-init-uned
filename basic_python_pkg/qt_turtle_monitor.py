import sys
import rclpy
from rclpy.node import Node

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

from geometry_msgs.msg import Twist


class TurtleMonitor(Node):

    def __init__(self, label):
        super().__init__('qt_turtle_monitor')

        self.label = label

        self.subscription = self.create_subscription(
            Twist,
            '/turtle1/cmd_vel',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        text = f"Linear: {msg.linear.x:.2f} | Angular: {msg.angular.z:.2f}"
        self.label.setText(text)


class MonitorWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Monitor Turtle")

        self.label = QLabel("Esperando datos...")

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)


def main():
    rclpy.init()

    app = QApplication(sys.argv)

    window = MonitorWindow()
    window.show()

    node = TurtleMonitor(window.label)

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
