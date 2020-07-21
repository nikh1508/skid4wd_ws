#!/usr/bin/env python

import rospy
from skid4wd_control import RobotControl
import misc_func.utils as utils

rospy.init_node('robot_control')
robot = RobotControl()

# First move to 0 degrees
rospy.loginfo('Rotating to 0 degrees')
robot.rotate_to(0, max_vel=0.5)

angle_now = 0.

for i in range(4):
    pose_start = robot.get_pose_abs()
    rospy.loginfo('Moving forward')
    robot.move_forward(bg=True)
    while utils.get_dist(robot.get_pose_abs(), pose_start) < 2.:
        rospy.sleep(.2)
    rospy.loginfo('Stopping Now')
    robot.stop()
    angle_now = (angle_now + 90.) % 360.
    rospy.loginfo('Rotating to ' + str(angle_now) + ' degrees')
    robot.rotate_to(angle_now, max_vel=0.5)

robot.exit()