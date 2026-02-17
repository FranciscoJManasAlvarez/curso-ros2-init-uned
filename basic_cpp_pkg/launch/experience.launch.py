import os
import pathlib
import launch
import yaml
import datetime
import shutil
from yaml.loader import SafeLoader
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions.path_join_substitution import PathJoinSubstitution
from launch import LaunchDescription


def get_ros2_nodes(context, *args):
    use_sim_time = LaunchConfiguration('use_sim_time', default=False)
    node_list = []

    file = LaunchConfiguration('config_file')
    file_name = file.perform(context)

    general_package_dir = get_package_share_directory('basic_cpp_pkg')
    config_path = os.path.join(general_package_dir, 'resources', file_name)
    with open(config_path, 'r') as file:
            documents = yaml.safe_load(file)

    for agent in documents['Nodes']:
        if documents['Nodes'][agent]['enable']:
            node = Node(
                package=documents['Nodes'][agent]['pkg'],
                executable=documents['Nodes'][agent]['executable'],
                name=documents['Nodes'][agent]['name'],
                namespace=documents['Nodes'][agent]['namespace'],
                parameters=[
                    {'use_sim_time': use_sim_time},
                ],
            )
            node_list.append(node)
    
    #----------------------#
    #     Data Logging     #
    #----------------------#
    if documents['Data_Logging']['enable']:
        e = datetime.datetime.now()
        if documents['Data_Logging']['all']:
            if documents['Data_Logging']['name'] == 'date':
                node_list.append(ExecuteProcess(
                    cmd=['ros2', 'bag', 'record', '-a', '-o', e.strftime("%Y-%m-%d-%H-%M")], output='screen', shell=True
                ))
            else:
                node_list.append(ExecuteProcess(
                    cmd=['ros2', 'bag', 'record', '-a', '-o', documents['Data_Logging']['name']], output='screen', shell=True
                ))
        else:
            if documents['Data_Logging']['name'] == 'date':
                node_list.append(ExecuteProcess(
                    cmd=['ros2', 'bag', 'record', '-o', e.strftime("%Y-%m-%d-%H-%M"), documents['Data_Logging']['topics']], output='screen', shell=True
                ))
            else:
                node_list.append(ExecuteProcess(
                    cmd=['ros2', 'bag', 'record', '-o', documents['Data_Logging']['name'], documents['Data_Logging']['topics']], output='screen', shell=True
                ))

    return node_list

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'config_file',
            default_value='demo_file.yaml',
            description='path config file'
        ),
        launch.actions.OpaqueFunction(function=get_ros2_nodes),
    ])