#  Utility functions

# Mapping input to new range
def map(x, in_low, in_high, out_low, out_high):
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