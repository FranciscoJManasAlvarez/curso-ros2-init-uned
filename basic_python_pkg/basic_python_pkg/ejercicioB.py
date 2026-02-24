# node_b_service.py
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class ServiceNodeB(Node):

    def __init__(self):
        super().__init__('node_b')
        self.srv = self.create_service(
            AddTwoInts,
            'b_service',
            self.service_callback
        )
        self.get_logger().info('Servicio B listo.')

    def service_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(
            f'Recibido: {request.a} + {request.b} = {response.sum}'
        )
        return response


def main():
    rclpy.init()
    node = ServiceNodeB()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()