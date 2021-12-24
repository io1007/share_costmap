#include <ros/ros.h>
#include <geometry_msgs/PointStamped.h>
#include <sensor_msgs/Range.h>
#include <tf/transform_listener.h>

void transformPoint(const tf::TransformListener& listener){
  //we'll create a point in the base_laser frame that we'd like to transform to the base_link frame
  geometry_msgs::PointStamped laser_point;
  sensor_msgs::Range sonar_point;
  sonar_point.header.frame_id = "base_sonar";

  //we'll just use the most recent transform available for our simple example
  sonar_point.header.stamp = ros::Time();

  //just an arbitrary point in space
  sonar_point.range = 1;

  try{
    geometry_msgs::PointStamped base_point;
    /*
    listener.transformPoint("base_link", sonar_point, base_point);

    ROS_INFO("base_sonar: (%.2f) -----> base_link: (%.2f) at time %.2f",
        sonar_point.range,base_point.range, base_point.header.stamp.toSec());
    */
  }
  catch(tf::TransformException& ex){
    ROS_ERROR("Received an exception trying to transform a point from \"base_laser\" to \"base_link\": %s", ex.what());
  }
}

int main(int argc, char** argv){
  ros::init(argc, argv, "sonar_tf_listener");
  ros::NodeHandle n;

  tf::TransformListener listener(ros::Duration(10));

  //we'll transform a point once every second
  ros::Timer timer = n.createTimer(ros::Duration(1.0), boost::bind(&transformPoint, boost::ref(listener)));

  ros::spin();

}
