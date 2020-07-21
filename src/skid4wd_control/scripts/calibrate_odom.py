#!/usr/bin/env python

# The purpose of this script is to get the difference between the angular velocities obtained from the /odom topic
# and from /gazebo/get_model_state service, in order for them to be calibrated to make the difference as close to
# zero as possible

import rospy
import signal
import time
import math
from skid4wd_control import RobotControl
from gazebo_msgs.srv import GetModelState, GetModelStateRequest
from nav_msgs.msg import Odometry

rospy.init_node('odom_calibration')
r = RobotControl()
odom = Odometry()
rospy.wait_for_service('/gazebo/get_model_state')

pos_service = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
model_state = GetModelStateRequest()
model_state.model_name = 'skid4wd'

def odom_cb(msg):
    global odom
    odom = msg

rospy.Subscriber('/skid4wd/drive_controller/odom', Odometry, odom_cb)
r.move(speed_angular=1.,bg=True)

def w_abs():
    result = pos_service(model_state)
    return result.twist.angular.z

def w_odom():
    return odom.twist.twist.angular.z

rate = rospy.Rate(5)

while True:
    print w_abs(), w_odom()
    rate.sleep()