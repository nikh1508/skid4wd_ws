#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from gazebo_msgs.srv import GetModelState, GetModelStateRequest
import misc_func.utils as utils 

import time
import math
import threading
import signal
import sys


class RobotControl():

    def __init__(self, model_name='skid4wd' ,cmd_vel='/skid4wd/drive_controller/cmd_vel', odom='/skid4wd/drive_controller/odom'):
        
        self._twist = Twist()
        self._model_state = GetModelStateRequest()
        self._rate = rospy.Rate(10)
        
        self._pub_vel = rospy.Publisher(cmd_vel, Twist, queue_size=1)
        self._sub_odom = rospy.Subscriber(odom, Odometry, self._odom_cb)
        self._get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        
        self._model_state.model_name = model_name
        self._send_vel_bg = False
        self._vel_thread = threading.Thread(target=self._vel_bg)
        self._odom = None
        signal.signal(signal.SIGINT, self.exit)
        
        while self._odom is None:   # Wait for Odometry
            rospy.loginfo('Waiting for odometry')
            rospy.sleep(1.)
        rospy.loginfo('Robot initialized')

    # This function keeps sending the twist messages in the background, since the diff_drive_controller has a cmd_vel timeout
    def _vel_bg(self):
        while self._send_vel_bg and not rospy.is_shutdown():
            self._pub_vel.publish(self._twist)
            self._rate.sleep()

    def _odom_cb(self, msg):
        self._odom = msg
    
    def stop(self):
        self._twist.linear.x = self._twist.angular.z = 0.0
        self._pub_vel.publish(self._twist)

    def move(self, speed_linear=0.0, speed_angular=0.0, tend=-1, bg=False):
        self._twist.linear.x = speed_linear
        self._twist.angular.z = speed_angular

        tstart = time.time()
        self._pub_vel.publish(self._twist)
        
        if not bg and tend > 0:
            while time.time() - tstart < tend:
                self._pub_vel.publish(self._twist)
                self._rate.sleep()
            self.stop()
        elif bg:
            self._send_vel_bg = True
            if not self._vel_thread.is_alive():
                self._vel_thread.start()
        
    def move_forward(self, speed=0.5, tend=-1, bg=False):
        self.move(speed_linear=speed, tend=tend, bg=bg)
    
    def get_yaw(self):
        (roll, pitch, yaw) = utils.quat2euler(self._odom.pose.pose.orientation, True)
        yaw = abs(yaw) if yaw < 0. else abs(yaw - 360.)
        return yaw

    def get_yaw_abs(self):
        result = self._get_model_state(self._model_state)
        (roll, pitch, yaw) = utils.quat2euler(result.pose.orientation, True)
        yaw = abs(yaw) if yaw < 0. else abs(yaw - 360.)
        return yaw

    def get_pose(self):
        return self._odom.pose.pose.position
    
    def get_pose_abs(self):
        odom_abs = self._get_model_state(self._model_state)
        return odom_abs.pose.position

    def rotate_to(self, heading, kp = 0.5, max_vel=0.2):
        while abs(self.get_yaw_abs() - heading) > 2: # +-5 degrees
            self.move(speed_angular=utils.constrain(kp*utils.angle_diff(self.get_yaw_abs(), heading), -max_vel, max_vel))
            # print "In:", self.get_yaw_abs(), " Set:", heading
            self._rate.sleep()
        self.stop()

    def exit(self, sig=None, frame=None):
        self.stop()
        self._send_vel_bg = False
        rospy.loginfo('\nStopping the robot and exiting...')
        self._vel_thread.join()
        sys.exit(0)