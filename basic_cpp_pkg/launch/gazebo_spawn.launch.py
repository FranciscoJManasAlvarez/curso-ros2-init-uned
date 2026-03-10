import os
import xacro
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)
    general_package_dir = get_package_share_directory('basic_cpp_pkg')
    config_path = os.path.join(general_package_dir, 'config', 'bridge_spawn.yaml')
    world_path = os.path.join(general_package_dir, 'worlds', 'empty_world.sdf')
    urdf_file = os.path.join(general_package_dir, 'model', 'robot_diferencial.urdf')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo','-r', '-v', '4', '--render-engine', 'ogre', world_path],
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
    
    robot_description = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

        # Crear robot en Gazebo
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[ '-name', 'robot_diferencial',
                    '-topic', 'robot_description',
                    '-x', '0.0',
                    '-y', '0.0',
                    '-z', '0.1'
        ],
        output='screen'
    )
    
    
    return LaunchDescription([
        gazebo,
        bridge_node,
        interface,
        robot_description,
        spawn
    ])