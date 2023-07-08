cmake_minimum_required(VERSION 2.8.3)

project(robot_assembly)

find_package(catkin REQUIRED
rospy
std_msgs
sensor_msgs
)

catkin_package()

find_package(roslaunch)

foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)

catkin_install_python(PROGRAMS src/pid_controller.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
