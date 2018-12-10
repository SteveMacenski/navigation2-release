#!/usr/bin/env python3

# Copyright (c) 2018 Intel Corporation
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
import sys

from launch import LaunchDescription
from launch import LaunchService
import launch.actions
from launch.actions import ExecuteProcess
import launch_ros.actions
from launch_testing import LaunchTestService


def main(argv=sys.argv[1:]):
    mapFile = os.getenv('TEST_MAP')
    testExecutable = os.getenv('TEST_EXECUTABLE')
    world = os.getenv('TEST_WORLD')

    launch_gazebo = launch.actions.ExecuteProcess(
        cmd=['gzserver', '-s', 'libgazebo_ros_init.so', world],
        output='screen')
    link_footprint = launch_ros.actions.Node(
        package='tf2_ros',
        node_executable='static_transform_publisher',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'base_footprint', 'base_link'])
    footprint_scan = launch_ros.actions.Node(
        package='tf2_ros',
        node_executable='static_transform_publisher',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'base_scan'])
    run_map_server = launch_ros.actions.Node(
        package='nav2_map_server',
        node_executable='map_server',
        node_name='map_server',
        output='screen',
        parameters=[{'yaml_filename': mapFile}])
    run_amcl = launch_ros.actions.Node(
        package='nav2_amcl',
        node_executable='amcl',
        output='screen')
    ld = LaunchDescription([launch_gazebo, link_footprint, footprint_scan,
                            run_map_server, run_amcl])

    test1_action = ExecuteProcess(
        cmd=[testExecutable],
        name='test_localization_node',
        output='screen'
    )
    ld.add_action(test1_action)
    lts = LaunchTestService()
    lts.add_test_action(ld, test1_action)
    ls = LaunchService(argv=argv)
    ls.include_launch_description(ld)
    return lts.run(ls)


if __name__ == '__main__':
    sys.exit(main())
