import os
import random
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess, TimerAction, LogInfo
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Configuración
    N = 3
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)
    general_package_dir = get_package_share_directory('basic_cpp_pkg')
    world_path = os.path.join(general_package_dir, 'worlds', 'empty_world.sdf')
    urdf_file = os.path.join(general_package_dir, 'model', 'robot_diferencial.urdf')
    rviz_config = os.path.join(general_package_dir, 'config', 'map_odom.rviz')

    # Leer el URDF
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Generar posiciones aleatorias
    random.seed(42)
    robot_poses = []
    for i in range(N):
        pose = {
            'name': f'robot_{i+1}',
            'x': random.uniform(-3.0, 3.0),
            'y': random.uniform(-3.0, 3.0),
            'z': 0.1,
            'yaw': random.uniform(0, 6.28)
        }
        robot_poses.append(pose)

    # Iniciar Gazebo
    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', '-v', '4', '--render-engine', 'ogre', world_path],
        output='screen'
    )

    # Bridge principal
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='parameter_bridge',
        output='screen',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry@ignition.msgs.Odometry',
            '/clock@rosgraph_msgs/msg/Clock@ignition.msgs.Clock'
        ],
        remappings=[
            ('/odom', '/odom_raw')  # Renombramos la odometría cruda
        ]
    )
    
    # Transform estático map → odom (si odom es relativo a map)
    static_tf_map_to_odom = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_map_to_odom',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']
    )
    
    # Nodo para transformar odom → base_link usando la odometría
    # (esto normalmente lo hace robot_localization, pero podemos simularlo)
    
    # RViz2 con configuración específica
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config] if os.path.exists(rviz_config) else [],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    launch_actions = [
        gazebo,
        bridge_node,
        static_tf_map_to_odom,
        rviz_node,
        LogInfo(msg=f'===== Spawneando {N} robots con marco map =====')
    ]

    # Publicador de robot_description
    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': use_sim_time,
            'frame_prefix': ''  # Importante: sin prefijo para base_link
        }],
        output='screen'
    )
    launch_actions.append(robot_state_pub)

    # Spawnear robots
    for i, pose in enumerate(robot_poses):
        log_msg = LogInfo(msg=f'Robot {pose["name"]} en [{pose["x"]:.2f}, {pose["y"]:.2f}]')
        launch_actions.append(log_msg)
        
        spawn_delay = 3.0 + (i * 2.0)
        spawn_robot = TimerAction(
            period=spawn_delay,
            actions=[
                Node(
                    package='ros_gz_sim',
                    executable='create',
                    arguments=[
                        '-name', pose['name'],
                        '-topic', 'robot_description',
                        '-x', str(pose['x']),
                        '-y', str(pose['y']),
                        '-z', str(pose['z']),
                        '-Y', str(pose['yaw'])
                    ],
                    output='screen'
                )
            ]
        )
        launch_actions.append(spawn_robot)

    return LaunchDescription(launch_actions)