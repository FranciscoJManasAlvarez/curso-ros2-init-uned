import rclpy
from rclpy.node import Node
from std_msgs.msg import String, UInt16MultiArray, Float64, Float64MultiArray, MultiArrayDimension


class CurseNode(Node):
    def __init__(self):
        super().__init__('demo_node_py')
        # Params
        self.declare_parameter('example_param', 'value')

        # Publisher
        self.publisher_example_ = self.create_publisher(String,'/topic_cpp', 10)
        
        # Subscription
        self.sub_example = self.create_subscription(String, '/topic_py', self.example_callback, 10)
        
        self.initialize()
    
    def initialize(self):
        self.get_logger().info('CurseExample::inicialize() ok.')
        self.i = 1
        self.timer = self.create_timer(0.5, self.iterate)

    def example_callback(self, msg):
        data = msg.data
        self.get_logger().info('New msg py: %s' % (data))

    def iterate(self):
        msg = String()
        msg.data = 'Mensaje '+str(self.i)
        self.publisher_example_.publish(msg)
        self.get_logger().warn('%s' % msg.data)
        self.i += 1



def main(args=None):
    rclpy.init(args=args)
    basic_node = CurseNode()
    rclpy.spin(basic_node)

    basic_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

