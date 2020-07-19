#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler

import time
import math
import threading
import signal
import sys


class RobotControl():

    def __init__(self ,cmd_vel='/skid4wd/drive_controller/cmd_vel', odom='/skid4wd/drive_controller/odom'):
        
        self._twist = Twist()
        self._rate = rospy.Rate(10)
        self._pub_vel = rospy.Publisher(cmd_vel, Twist, queue_size=1)
        self._sub_odom = rospy.Subscriber(odom, Odometry, self._odom_cb)
        self._send_vel_bg = False
        self._vel_thread = threading.Thread(target=self._vel_bg)
        self._odom = Odometry()
        signal.signal(signal.SIGINT, self.exit)

    # This function keeps sending the twist messages in the background, since the diff_drive_controller has a cmd_vel timeout
    def _vel_bg(self):
        while self._send_vel_bg and not rospy.is_shutdown():
            self._pub_vel.publish(self._twist)
            self._rate.sleep()

    def _odom_cb(self, msg):
        self._odom = msg
    
    def stop(self):
        self._send_vel_bg = False
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
            self._vel_thread.start()
        
    def move_forward(self, speed=0.5, tend=-1, bg=False):
        self.move(speed_linear=speed, tend=tend, bg=bg)
    
    def get_yaw(self):
        _q = self._odom.pose.pose.orientation
        (roll, pitch, yaw) = euler_from_quaternion([_q.x, _q.y, _q.z, _q.w])
        return yaw / math.pi * 180.

    def _get_diff(self, _inp, _set):
        tmp = abs(_inp - _set)
        diff = min(tmp, abs(360 - tmp))
        if (_set + diff) != _inp and (_set - diff) != _inp:
            if (_inp + diff) >= 360:
                    return -diff
            else: 
                return diff
        else:
            return _inp - _set

    def rotate_to(self, heading, kp = 0.5):
        while abs(self.get_yaw() - heading) > 5: # +-5 degrees
            self.move(speed_angular=-kp*self._get_diff(self.get_yaw(), heading))
            self._rate.sleep()
        self.stop()

    def exit(self, sig, frame):
        self.stop()
        print '\nStopping the robot and exiting...'
        sys.exit(0)