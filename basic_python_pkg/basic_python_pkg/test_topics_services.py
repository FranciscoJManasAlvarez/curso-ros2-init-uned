import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import String, UInt16MultiArray, Float64, Float64MultiArray, MultiArrayDimension
from basic_cpp_pkg.msg import Actuators
from basic_cpp_pkg.srv import TestDelay
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy, QoSHistoryPolicy


class CurseNode(Node):
    def __init__(self):
        super().__init__('demo_node_py')
        # Params
        self.declare_parameter('example_param', 'value')

        # Publisher
        self.publisher_example_ = self.create_publisher(String,'/topic_cpp', 10)
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,         # o BEST_EFFORT
            durability=QoSDurabilityPolicy.VOLATILE,           # o TRANSIENT_LOCAL
            history=QoSHistoryPolicy.KEEP_LAST,                # o KEEP_ALL
            depth=10                                            # tamaño del buffer
        )
        self.publisher_msg_propio_ = self.create_publisher(Actuators,'/actuators', qos_profile)
        
        # Subscription
        self.sub_example = self.create_subscription(String, '/topic_py', self.example_callback, 10)
        
        # Service 
        self.srv_ = self.create_service(TestDelay, '/test_delay', self.testdelay_callback)

        self.initialize()
    
    def initialize(self):
        self.get_logger().info('CurseExample::inicialize() ok.')
        self.i = 1
        self.timer = self.create_timer(0.5, self.iterate)

    def example_callback(self, msg):
        data = msg.data
        self.get_logger().info('New msg py: %s' % (data))

    def testdelay_callback(self, request, response):
        time_now = self.get_clock().now().nanoseconds
        response.delay = time_now - request.a
        self.get_logger().info('Incoming request\nDelay: %f' % (response.delay))
        time.sleep(5)
        return response

    def iterate(self):
        msg = String()
        msg.data = 'Mensaje '+str(self.i)
        self.publisher_example_.publish(msg)
        self.get_logger().warn('%s' % msg.data)
        self.i += 1
        if self.i == 4:
            msg = Actuators()
            msg.angles = [10.0, 2.1, 5.36, 3.14]
            msg.flags = [True, False, False, True]
            msg.id = 'sensor01'
            self.publisher_msg_propio_.publish(msg)
            self.i = 1



def main(args=None):
    rclpy.init(args=args)
    basic_node = CurseNode()
    rclpy.spin(basic_node)

    basic_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

