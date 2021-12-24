#! /usr/bin/env python
#import roslib
#roslib.load_manifest('sonar_test')

import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import Range 
import RPi.GPIO as GPIO
import time
import sys
import tf

class Sonar():

    def __init__(self,radiation_type=0,min_range=0.00,max_range=4.00):
        
        #Define variables
        self.radiation_type = radiation_type
        self.min_range = min_range
        self.max_range = max_range
        self.h = Header()

        #Initialize node
        rospy.init_node("sonar_sensor")
        #Initialize Publisher
        #self.distance_pub = rospy.Publisher("/rspi/sonar",Range,queue_size=1)
        self.distance_pub = rospy.Publisher("/turtlebot3/ultrasound",Range,queue_size=1)
        #loop_rate
        self.rate = rospy.Rate(10)

        self.br = tf.TransformBroadcaster()

    def dist_sendor(self,dist):
        msg = Range()
        msg.range = dist/100
        #msg.radiation_type = self.radiation_type
        msg.min_range = self.min_range
        msg.max_range = self.max_range
        self.h.stamp = rospy.Time.now()
        self.h.frame_id = "base_sonar"
        msg.field_of_view = 25*3.14/180
        msg.header = self.h
        self.distance_pub.publish(msg)
        rospy.loginfo( "Distance:{}m".format(str(msg.range)))

    def get_sonar(self):

        GPIO.setmode(GPIO.BCM)

        TRIG = 17 
        ECHO = 27

        print "Distance Measurement In Progress"

        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)


        while not rospy.is_shutdown():

            GPIO.output(TRIG, False)
            print "Waiting For Sensor To Settle"
            time.sleep(0.1)

            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO)==0:
              pulse_start = time.time()

            while GPIO.input(ECHO)==1:
              pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)

            self.dist_sendor(distance)
            """
            t = rospy.Time.now().to_sec()
            self.br.sendTransform((0.0,0.0,0.3),
                    (0.0,0.0,0.0,1.0),
                    rospy.Time.now(),
                    "base_sonar",
                    "base_link")
            """

            self.rate.sleep()

            #GPIO.cleanup(TRIG)
            #GPIO.cleanup(ECHO)

if __name__ == '__main__':
    try:
        sensor = Sonar()
        sensor.get_sonar()
    except rospy.ROSInterruptException:
        GPIO.cleanup(TRIG)
        GPIO.cleanup(ECHO)
        sys.exit(0)
