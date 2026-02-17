cmake_minimum_required(VERSION 3.8)
project(basic_cpp_pkg)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rclpy REQUIRED)
find_package(urdf REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Actuators.msg"
  "srv/AddTwoInts.srv"
)

#############
## Install ##
#############

install(
  DIRECTORY
    launch
    model
    resources
    rviz
    rqt
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS
  DESTINATION lib/${PROJECT_NAME}
)

add_executable(basic_node src/basic_node.cpp)
ament_target_dependencies(basic_node
    rclcpp std_msgs sensor_msgs geometry_msgs)

add_executable(demo_node src/demo_node.cpp)
ament_target_dependencies(demo_node
    rclcpp std_msgs sensor_msgs geometry_msgs)

install(TARGETS basic_node demo_node
  DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION include)

ament_package()
