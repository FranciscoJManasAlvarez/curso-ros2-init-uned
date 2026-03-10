import os
import random
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess, TimerAction, LogInfo
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Configuración
    N = 5  # Número de robots a spawnear (puedes cambiar este valor)
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)
    general_package_dir = get_package_share_directory('basic_cpp_pkg')
    config_path = os.path.join(general_package_dir, 'config', 'bridge_spawn.yaml')
    world_path = os.path.join(general_package_dir, 'worlds', 'empty_world.sdf')
    urdf_file = os.path.join(general_package_dir, 'model', 'robot_diferencial.urdf')

    # Leer el URDF
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Generar posiciones aleatorias para los robots
    random.seed(42)  # Para reproducibilidad, opcional
    robot_poses = []
    for i in range(N):
        pose = {
            'name': f'robot_{i+1}',
            'x': random.uniform(-5.0, 5.0),
            'y': random.uniform(-5.0, 5.0),
            'z': 0.1,
            'yaw': random.uniform(0, 6.28)  # Rotación aleatoria
        }
        robot_poses.append(pose)

    # Iniciar Gazebo
    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', '-v', '4', '--render-engine', 'ogre', world_path],
        output='screen'
    )

    # Bridge node
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='parameter_bridge',
        output='screen',
        parameters=[{
            "config_file": config_path
        }]
    )
    
    # RViz2
    interface = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        parameters=[
            {'use_sim_time': use_sim_time},
        ]
    )
    
    # Robot State Publisher (publica el modelo URDF en /robot_description)
    robot_description_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # Lista para almacenar todas las acciones
    launch_actions = [
        gazebo,
        bridge_node,
        interface,
        robot_description_node,
        LogInfo(msg=f'===== Spawneando {N} robots en posiciones aleatorias =====')
    ]

    # Spawnear robots con TimerAction para espaciarlos en el tiempo
    for i, pose in enumerate(robot_poses):
        # Log de la posición
        log_msg = LogInfo(
            msg=f'Robot {pose["name"]} - Posición: x={pose["x"]:.2f}, y={pose["y"]:.2f}, yaw={pose["yaw"]:.2f}'
        )
        launch_actions.append(log_msg)
        
        # Spawn del robot después de un delay (3 segundos para el primero, luego cada 0.5 segundos)
        spawn_delay = 3.0 + (i * 0.5)
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
                        '-Y', str(pose['yaw'])  # Yaw para orientación
                    ],
                    output='screen'
                )
            ]
        )
        launch_actions.append(spawn_robot)

    return LaunchDescription(launch_actions)