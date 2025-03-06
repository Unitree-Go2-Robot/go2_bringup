# Copyright (c) 2024 Intelligent Robotics Lab (URJC)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def start_hesai_lidar(context):
    if (LaunchConfiguration('hesai_lidar').perform(context) == 'true' or
            LaunchConfiguration('hesai_lidar').perform(context) == 'True'):
        return [IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('hesai_ros_driver'),
                'launch/'), 'start.py'])
        )]

    return []


def start_livox_lidar(context):
    if (LaunchConfiguration('livox_lidar').perform(context) == 'true' or
            LaunchConfiguration('livox_lidar').perform(context) == 'True'):
        return [IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('livox_ros_driver2'),
                'launch/'), 'rviz_MID360_launch.launch.py'])
        )]

    return []


def start_realsense(context):
    if (LaunchConfiguration('realsense').perform(context) == 'true' or
            LaunchConfiguration('realsense').perform(context) == 'True'):
        return [IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('realsense2_camera'),
                'launch/'), 'rs_launch.py'])
        )]

    return []


def generate_launch_description():

    declare_hesai_cmd = DeclareLaunchArgument(
        'hesai_lidar',
        default_value='false',
        description='Launch hesai lidar driver'
    )

    declare_livox_cmd = DeclareLaunchArgument(
        'livox_lidar',
        default_value='false',
        description='Launch livox lidar driver'
    )

    declare_realsense_cmd = DeclareLaunchArgument(
        'realsense',
        default_value='false',
        description='Launch realsense driver'
    )

    declare_rviz_cmd = DeclareLaunchArgument(
        'rviz',
        default_value='False',
        description='Launch rviz'
    )

    robot_description_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('go2_description'),
            'launch/'), 'robot.launch.py'])
    )

    driver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('go2_driver'),
            'launch/'), 'go2_driver.launch.py'])
    )

    rviz_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('go2_rviz'),
            'launch/'), 'rviz.launch.py']),
        condition=IfCondition(LaunchConfiguration('rviz'))
    )

    ld = LaunchDescription()
    ld.add_action(declare_hesai_cmd)
    ld.add_action(declare_livox_cmd)
    ld.add_action(declare_realsense_cmd)
    ld.add_action(declare_rviz_cmd)
    ld.add_action(robot_description_cmd)
    ld.add_action(driver_cmd)
    ld.add_action(OpaqueFunction(function=start_hesai_lidar))
    ld.add_action(OpaqueFunction(function=start_livox_lidar))
    ld.add_action(OpaqueFunction(function=start_realsense))
    ld.add_action(rviz_cmd)

    return ld
