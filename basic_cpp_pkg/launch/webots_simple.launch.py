import os
import pathlib
import launch
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.utils import controller_url_prefix
from webots_ros2_driver.webots_controller import WebotsController


def generate_launch_description():
    package_dir = get_package_share_directory('basic_webots_pkg')
    general_package_dir = get_package_share_directory('basic_cpp_pkg')
    use_sim_time = LaunchConfiguration('use_sim_time', default=False)
    webots = WebotsLauncher(
        world=os.path.join(general_package_dir, 'worlds', 'simple_world.wbt')
    )

    robot_description = os.path.join(package_dir, 'resource', 'robot.urdf')
    with open(robot_description, 'r') as infp:
        robot_desc = infp.read()
    aux = robot_desc.replace("demo_robot", 'robot01')
    aux = aux.replace("name_id_value", 'robot01')

    robot_controller = WebotsController(
                            parameters=[
                                {'robot_description': aux,
                                'use_sim_time': use_sim_time,
                                'set_robot_state_publisher': True},
                            ],
                            respawn=True
                        )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': '<robot name=""><link name=""/></robot>'
        }],
    )

    rqt_node = Node(
        package='rqt_gui',
        executable='rqt_gui',
        name='interface',
        parameters=[
            {'use_sim_time': use_sim_time},
        ],
    )

    return LaunchDescription([
        webots,
        robot_controller,
        rqt_node,
        robot_state_publisher,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])
