# node_a_client.py
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from example_interfaces.action import Fibonacci
from example_interfaces.srv import AddTwoInts


class ClientNodeA(Node):

    def __init__(self):
        super().__init__('node_a')

        self.client_b = self.create_client(AddTwoInts, 'b_service')
        while not self.client_b.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando al servicio B...')

        self.action_client = ActionClient(
            self,
            Fibonacci,
            'c_action'
        )

        self.send_goal()

    def send_goal(self):
        self.action_client.wait_for_server()

        goal = Fibonacci.Goal()
        goal.order = 5

        self.get_logger().info('Enviando goal a C...')
        self.action_client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )

    def feedback_callback(self, feedback_msg):
        remaining = feedback_msg.feedback.sequence[0]
        self.get_logger().info(
            f'Feedback recibido: quedan {remaining} iteraciones'
        )


def main():
    rclpy.init()
    node = ClientNodeA()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()