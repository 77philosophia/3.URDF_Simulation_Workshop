#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from tf2_ros import StaticTransformBroadcaster
# message that used in tf static 
from geometry_msgs.msg import TransformStamped

class TFStaticExample(Node):
    
    def __init__(self):
        # Initialize the node
        super().__init__('tf_static_node')
        
        # instance from static transform broadcaster class 
        # need this object to publish static transform in TF static topic
        self.static_broadcaster = StaticTransformBroadcaster(self)
        
        # create a static transform message
        self.static_transform_stamped = TransformStamped()
        
        # add information about time when this static transform has been generated
        self.static_transform_stamped.header.stamp = self.get_clock().now().to_msg()
        
        # as we learn that tf connect two frames together
        # let's define the parent frame and the child frame 
        
        # parent frame
        self.static_transform_stamped.header.frame_id = "base_link"
        # child frame any frame like laser of camera or any other frame
        # important to note that the child frame should be static frame
        self.static_transform_stamped.child_frame_id = "laser" 
        
        # we know that child frame is connected to parent frame by translation and rotation vectors
        # let's define translation vectors
        self.static_transform_stamped.transform.translation.x = 0.0
        self.static_transform_stamped.transform.translation.y = 0.0
        # in z axes 10 cm above the base_link frame
        self.static_transform_stamped.transform.translation.z = 0.1
        
        # let's define rotation vectors 
        self.static_transform_stamped.transform.rotation.x = 0.0
        self.static_transform_stamped.transform.rotation.y = 0.0
        self.static_transform_stamped.transform.rotation.z = 0.0
        self.static_transform_stamped.transform.rotation.w = 1.0
        
        # Send the transform
        self.static_broadcaster.sendTransform(self.static_transform_stamped)
        self.get_logger().info("TF static has been published between %s and %s frames" % (
            self.static_transform_stamped.header.frame_id, 
            self.static_transform_stamped.child_frame_id
        ))
        
def main():
    # Initialize ROS2
    rclpy.init()
    
    # Create the node
    node = TFStaticExample()
    
    # Since static transforms are published once and remain in the system,
    # we don't need to spin continuously. But we keep the node alive.
    try:
        # Keep the node running to maintain the transform
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()