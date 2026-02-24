import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster
import math

class CombinedTFPublisher(Node):
    def __init__(self):
        super().__init__('combined_tf_publisher')

        # Broadcasters
        self.tf_broadcaster = TransformBroadcaster(self)
        self.static_broadcaster = StaticTransformBroadcaster(self)

        # Publicar TF estática una vez
        self.publish_static_tf()

        # Temporizador para la TF dinámica
        self.angle = 0.0
        self.timer = self.create_timer(0.1, self.publish_dynamic_tf)

    def publish_static_tf(self):
        """Transformación estática: arm_link → camera_link"""
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'arm_link'
        t.child_frame_id = 'camera_link'

        # Cámara fija en la punta del brazo
        t.transform.translation.x = 0.3
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.static_broadcaster.sendTransform(t)
        self.get_logger().info('TF estática arm_link → camera_link publicada')

    def publish_dynamic_tf(self):
        """Transformación dinámica: base_link → arm_link"""
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'arm_link'

        # Brazo girando en yaw
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.5

        qz = math.sin(self.angle / 2.0)
        qw = math.cos(self.angle / 2.0)
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = qz
        t.transform.rotation.w = qw

        self.tf_broadcaster.sendTransform(t)
        self.angle += 0.05

def main():
    rclpy.init()
    node = CombinedTFPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()