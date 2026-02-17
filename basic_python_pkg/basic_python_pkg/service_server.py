import rclpy
import time
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from basic_cpp_pkg.srv import AddThreeInts


class MinimalServiceServer(Node):

    def __init__(self):
        super().__init__('minimal_service_server')
        self.srv = self.create_service(AddThreeInts, 'add_three_ints', self.add_three_ints_callback)

    def add_three_ints_callback(self, request, response):
        response.sum = request.a + request.b + request.c
        self.get_logger().info(f'Request: {request.a} + {request.b} + {request.c}')
        time.sleep(5)
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service_server = MinimalServiceServer()
    rclpy.spin(minimal_service_server)
    minimal_service_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()