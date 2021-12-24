#!/usr/bin/env python
import roslib
roslib.load_manifest('sonar_test')
import rospy
import tf
from sensor_msgs.msg import Range

class SonarListener:
    def __init__(self, *args):
        rospy.init_node("sonar_listener")
        self.tf_listener_ = tf.TransformListener()
        print 'hello'
        rospy.Subscriber("sonar",Range,self.sonar_cb)

    def sonar_cb(self,msg):
        print 'world'
        #if tf.frameExists("/base_link") and tf.frameExists("/base_sonar"):
        t = self.tf_listener_.getLatestCommonTime("/base_link", "/base_sonar")
        p1 = Range()
        p1.radiation_type = msg.radiation_type
        p1.min_range = msg.min_range
        p1.max_range = msg.max_range
        p1.header = msg.header
        p1.range = msg.range
        
        p_in_base = self.tf_listener_.transformPose("/base_link", p1)
        print "Position of the sonar in the robot base:"
        print p_in_base

if __name__ == '__main__':
    SonarListener()
    rospy.spin()
