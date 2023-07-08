# SelfBalancingRobot
Two-wheeled self-balancing robot realized for the Robotics course at Polito, academic year 2022-2023. The simulation is based on ROS Noetic and works on Ubuntu 20.04

# Run the Gazebo simulation
- Download the robot_assembly folder in your catkin workspace and run from a terminal: catkin_make
- Run from a terminal: roslaunch robot_assembly istagger_launch.launch
- After starting the simulation, the robot will initially fall. By rotating it upwards the PID controller will start working balancing the robot as prescribed
- You can tune the PID parameter by changing them in the Python file "pid_controller" under robot_assembly/src

# Run the Simscape simulation
- Download the Simscape folder
- Run the robot_assembly_simscape_DataFile in Matlab
- Open and run the robot_assembly.slx file to start the simulation
- You can tune the PID parameters changing them in the PID block

# Hardware implementation and Arduino code
Hardware details together with additional information on the project can be found in the Report_RoboticsProject_SelfBalancingRobot.pdf included in this repo.

The Arduino code can be uploaded through the Arduino IDE software and is intended for use on the Arduino Nano, but should also work with other similar boards. To correctly compile the program it is necessary to install the libraries linked at the beginning of the code by downloading them from GitHub and putting them under the Documents/Arduino/libraries folder.

Pin definitions in the code have to be changed depending on the connections with the driver and the motor. The PID parameters and the unstable equilibrium position used for reference can also be changed in the the program depending on the adopted hardware configuration.

