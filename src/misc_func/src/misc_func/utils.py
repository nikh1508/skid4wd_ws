#  Utility functions

import math
from tf.transformations import euler_from_quaternion, quaternion_from_euler

# Mapping input to new range
def map_val(x, in_low, in_high, out_low, out_high):
    return (float(x - in_low) / float(in_high - in_low) * (out_high - out_low)) + out_low

# Constrain input to given limits
def constrain(x, _min, _max):
    x = _max if x > _max else (_min if x < _min else x)
    return x

# Compare two floating point numbers
def isEqual(x, y):
    return (abs(x - y) < 1e-9)

# Get difference between two angles | Useful in case of a cycle of 360 degrees
# e.g. :
#       angle_diff(243.6, 11.0) = 127.4 | which is not equal to 11.0 - 243.6
def angle_diff(_inp, _set):
        tmp = abs(_inp - _set)
        diff = min(tmp, abs(360. - tmp))
        if not isEqual((_set + diff), _inp) and not isEqual((_set - diff), _inp):
            if (_inp + diff) >= 360:
                    return -diff
            else: 
                return diff
        else:
            return _inp - _set

def rad2deg(rad):
    return rad * 180. / math.pi

def deg2rad(deg):
    return deg * math.pi / 180.

def quat2euler(quat, in_degrees=False):
    (roll, pitch, yaw) = euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])
    return ([roll, pitch, yaw] if not in_degrees else map(rad2deg, [roll, pitch, yaw]))

def get_dist(pose_init, pose_final):
    return math.sqrt((pose_final.x - pose_init.x)**2 + (pose_final.y - pose_init.y)**2 + (pose_final.z - pose_init.z)**2)