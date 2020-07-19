#!/usr/bin/env python

import rospy
import signal
import time
import sys
from skid4wd_control import RobotControl


rospy.init_node('robot_control')
s = RobotControl()

# s.move(0.0, 1.0, bg=True)
s.rotate_to(90)

while True:
    print s.get_yaw()
rospy.spin()