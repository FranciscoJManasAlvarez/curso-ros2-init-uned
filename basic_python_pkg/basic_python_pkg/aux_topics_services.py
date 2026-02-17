import rclpy
from rclpy.node import Node
from std_msgs.msg import String, UInt16MultiArray, Float64, Float64MultiArray, MultiArrayDimension
from basic_cpp_pkg.msg import Actuators
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy, QoSHistoryPolicy


class CurseNode(Node):
    def __init__(self):
        super().__init__('demo_node_py')
        # Params
        self.declare_parameter('example_param', 'value')

        # Publisher
        self.publisher_example_ = self.create_publisher(String,'/status', 10)
        
        # Subscription
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,         # o BEST_EFFORT
            durability=QoSDurabilityPolicy.VOLATILE,           # o TRANSIENT_LOCAL
            history=QoSHistoryPolicy.KEEP_LAST,                # o KEEP_ALL
            depth=10                                            # tamaño del buffer
        )
        self.sub_example = self.create_subscription(Actuators, '/actuators', self.actuators_callback, qos_profile)
        
        self.initialize()
    
    def initialize(self):
        self.get_logger().info('CurseExample::inicialize() ok.')
        self.i = 1
        self.timer = self.create_timer(10, self.iterate)

    def actuators_callback(self, msg):
        id = msg.id
        angles = msg.angles
        self.get_logger().info('%s: %.2f : %.1f : %.3f' % (id, angles[0], angles[1], angles[2]))

    def iterate(self):
        data = 'Mensaje '+str(self.i)
        self.get_logger().warn('%s' % data)
        self.i += 1



def main(args=None):
    rclpy.init(args=args)
    basic_node = CurseNode()
    rclpy.spin(basic_node)

    basic_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

