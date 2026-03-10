import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)
    general_package_dir = get_package_share_directory('basic_cpp_pkg')
    config_path = os.path.join(general_package_dir, 'config', 'bridge.yaml')
    world_path = os.path.join(general_package_dir, 'worlds', 'visualize_lidar.sdf')

    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo','-r', world_path],
        output='screen'
    )

    bridge_node = Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='parameter_bridge',
            output='screen',
            parameters=[{
                "config_file": config_path
            }]
        )
    
    interface = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            parameters=[
                {'use_sim_time': use_sim_time},
            ]
        )
    transform = Node(
                package='tf2_ros',
                executable='static_transform_publisher',
                output='screen',
                name='robot',
                arguments=['--yaw', '3.1415', '--frame-id', '/vehicle_blue/lidar_link/gpu_lidar', '--child-frame-id', 'map'])

    return LaunchDescription([
        gazebo,
        bridge_node,
        interface,
        transform

    ])