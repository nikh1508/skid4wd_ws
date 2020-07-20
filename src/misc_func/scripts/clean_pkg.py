#!/usr/bin/env python

import sys
import os
import shutil

usage = '''
This script cleans all the unnecessary commented lines in CMakeLists.txt and package.xml of a newly created catkin package.
usage:
    rosrun misc_func clean_cmake.py [OPTION] [PATH]
    Options:
        -cmake : Clean CMakeLists.txt
        -xml : Clean package.xml
'''

args = len(sys.argv)

if args < 2 or sys.argv[1] not in ('-cmake', '-xml'):
    print usage
    sys.exit(-1) 

is_cmake = sys.argv[1] == '-cmake'
path = '.' if args == 2 else sys.argv[2]
to_edit = 'CMakeLists.txt' if is_cmake else 'package.xml'

try:
    files = os.listdir(path)
except:
    print 'Error:', sys.exc_info()[0]
    print usage
    sys.exit(-1)

if to_edit not in files:
    print "No '" + to_edit + "'found in the directory"
    sys.exit(-1)

prev_nl = False

def is_commented(line):
    if is_cmake:
        return line[0] == '#'
    else:
        return line.strip().startswith('<!--') and line.strip().endswith('-->')

with open(os.path.join(path, to_edit), 'r') as f:
    with open(os.path.join(path, 'tmp.tmp'), 'w') as ff:
        for line in f:
            if not is_commented(line):
                curr_nl = line[0] == '\n'
                if (curr_nl and not prev_nl) or not curr_nl:
                    ff.write(line)
                prev_nl = curr_nl

shutil.move(os.path.join(path, 'tmp.tmp'), os.path.join(path, to_edit))