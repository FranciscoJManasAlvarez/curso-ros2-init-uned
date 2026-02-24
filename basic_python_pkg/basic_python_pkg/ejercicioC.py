# node_c_action.py
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from example_interfaces.action import Fibonacci
from example_interfaces.srv import AddTwoInts


class ActionNodeC(Node):

    def __init__(self):
        super().__init__('node_c')

        self.action_server = ActionServer(
            self,
            Fibonacci,
            'c_action',
            self.execute_callback
        )

        self.client_b = self.create_client(AddTwoInts, 'b_service')
        while not self.client_b.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando al servicio B...')

        self.get_logger().info('Nodo C listo.')

    def execute_callback(self, goal_handle):
        self.get_logger().info('Acción iniciada.')

        feedback = Fibonacci.Feedback()
        result = Fibonacci.Result()

        iterations = 5

        for i in range(iterations):
            # Llamada al servicio B
            req = AddTwoInts.Request()
            req.a = i
            req.b = i

            future = self.client_b.call_async(req)
            rclpy.spin_until_future_complete(self, future)

            self.get_logger().info(
                f'Llamada a B realizada ({i+1}/{iterations})'
            )

            # Feedback a A
            remaining = iterations - (i + 1)
            feedback.sequence = [remaining]
            goal_handle.publish_feedback(feedback)

            time.sleep(1.0)

        goal_handle.succeed()
        result.sequence = [0]
        self.get_logger().info('Acción completada.')
        return result


def main():
    rclpy.init()
    node = ActionNodeC()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()