import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from basic_cpp_pkg.srv import AddThreeInts

class MinimalServiceClient(Node):

    def __init__(self):
        super().__init__('minimal_service_client')
        self.client = self.create_client(AddThreeInts, 'add_three_ints')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.request = AddThreeInts.Request()

    def send_request(self, a, b, c):
        self.request.a = a
        self.request.b = b
        self.request.c = c
        self.future = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    minimal_service_client = MinimalServiceClient()
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])
    response = minimal_service_client.send_request(a, b, c)
    minimal_service_client.get_logger().info(f'Result: {a} + {b} + {c} = {response.sum}')
    minimal_service_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()