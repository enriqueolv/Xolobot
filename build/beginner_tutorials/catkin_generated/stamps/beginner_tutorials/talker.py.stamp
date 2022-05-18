#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy
from std_msgs.msg import Float32MultiArray
# include <geometry_msgs/Twist.h>
from geometry_msgs.msg import Twist
from rosgraph_msgs.msg import Clock
from rospy.numpy_msg import numpy_msg
import numpy as np
from std_msgs.msg import Int32MultiArray
from arlo_nn_controller.srv import EvaluateDriver, EvaluateDriverResponse
import rospy

def proxy(maxTime):
    rospy.wait_for_service('evaluate_driver')
    try:
        evaluateDriver = rospy.ServiceProxy('evaluate_driver', EvaluateDriver)
        resp = evaluateDriver(5)
        # rospy.loginfo('I heard [',resp.dist2go)
        print(resp.dist2go)
        return resp
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def talker():
    
    pub = rospy.Publisher('gp_test', Float32MultiArray, queue_size=10)
    gPub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(50) # 10hz
    
    #mensaje 1
    msg1 = Twist()
    msg1.angular.z = 0.0
    msg1.linear.x = 0.1


    #mensaje 2
    msg2 = Twist()
    msg2.angular.z = 0.0
    msg2.linear.x = 0.0

    i=0
    while not rospy.is_shutdown():
        if (i%2) == 0:
            gPub.publish(msg1)
        else:
            gPub.publish(msg2)
        i = i+1

def main():
    try:
        talker()
        proxy(20)
    except rospy.ROSInterruptException as e:
        print(e)
        main()

if __name__ == '__main__':
    for i in range(5):
        main()