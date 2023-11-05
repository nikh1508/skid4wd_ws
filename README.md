# Four Wheel Skid Drive

Catkin Workspace for my own Four Wheel Skid Drive Simulation.
The packages in this workspace contains URDF Description and Controller for the robot.

<center><img src="images/render1.png" alt="Rendered Image" style="zoom: 40%;" /></center>

</br>



## Simulation

This repository is a catkin-workspace itself, therefore it can be cloned anywhere. To start the simulation in Gazebo do the below steps. [It is expected that all the required packages are already installed.]



```bash
git clone https://github.com/JITERN/skid4wd_ws.git
cd skid4wd_ws
source /opt/ros/noetic/setup.bash # change according to your ROS version
catkin build
source devel/setup.bash # or setup.zsh | depending on the shell you use

# Finally launch the simulation
roslaunch skid4wd_description sim_with_controller.launch
```



The simulation is started in paused state. Resume the simulation by clicking on the play button on the lower panel in Gazebo. 



To avoid sourcing the `setup.bash` files everytime you open a new terminal, copy these lines to your .zshrc or .bashrc :

```bash
source /opt/ros/noetic/setup.bash # or setup.zsh | depending on the shell you use
source {path to skid4wd}/devel/setup.bash
```



To steer the robot you can use `teleop_twist_keyboard` or `rqt_robot_steering`. To launch `rqt_robot_steering` run this on another terminal :

```bash
roslaunch skid4wd_description rqt_steering.launch
```



<center><img src="images/gazebo_sim.gif" style="zoom: 60%;"/></center>

</br>



## Visualize in RViz



To start RViz with proper configuration use the launch file provided. Make sure that the Gazebo simulation is unpaused, or RViz will give TF errors.

```bash
roslaunch skid4wd_description rviz.launch
```

 

<center><img src="images/rviz.gif" alt="RViz" style="zoom:60%;" /></center>

