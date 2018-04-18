cmake_minimum_required(VERSION 2.8.3)
project(mavlink_lora)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  roscpp
  rospy
  serial
  std_msgs
)

catkin_python_setup()

add_message_files(
  FILES
  mavlink_lora_msg.msg
 )

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS
  roscpp
  serial
  std_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(mavlink_lora_node src/mavlink_lora_node.cpp src/mavlink_lora_lib.c)

## Add cmake target dependencies of the executable/library
## as an example, message headers may need to be generated before nodes
add_dependencies(mavlink_lora_node mavlink_lora_generate_messages_cpp)


target_link_libraries(mavlink_lora_node
  ${catkin_LIBRARIES}
)

