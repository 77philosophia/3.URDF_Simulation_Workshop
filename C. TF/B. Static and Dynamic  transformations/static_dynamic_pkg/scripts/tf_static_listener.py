#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import TransformException, Buffer, TransformListener
from geometry_msgs.msg import TransformStamped

# 定义ROS 2节点类
class StaticTfListener(Node):

    def __init__(self):
        # 初始化节点
        super().__init__('static_tf_listener_ros2')
        
        # 帧名称
        self.target_frame = 'base_link'
        self.source_frame = 'laser'

        # 1. 创建 tf2 Buffer 和 TransformListener
        # Buffer 负责存储接收到的变换数据
        self.tf_buffer = Buffer()
        # TransformListener 监听 /tf 和 /tf_static 话题，并将数据馈送到 Buffer
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # 2. 创建定时器，每秒执行一次查询（代替 ROS 1 的 Rate 循环）
        # 频率设置为 1.0 Hz
        self.timer = self.create_timer(1.0, self.on_timer)
        self.get_logger().info(f"ROS 2 TF Listener started. Waiting for transform from '{self.source_frame}' to '{self.target_frame}'.")

    def on_timer(self):
        # 尝试查找坐标变换
        try:
            # 3. 使用 lookup_transform 查询变换
            # Time() 表示查询最新的可用变换 (相当于 ROS 1 的 rospy.Time(0))
            t: TransformStamped = self.tf_buffer.lookup_transform(
                self.target_frame,
                self.source_frame,
                Time()
            )
            
            # 4. 从 TransformStamped 消息中提取数据
            trans = t.transform.translation
            rot = t.transform.rotation
            
            self.get_logger().info(
                f"Translation: [{trans.x:.4f}, {trans.y:.4f}, {trans.z:.4f}], "
                f"Rotation (Quat): [{rot.x:.4f}, {rot.y:.4f}, {rot.z:.4f}, {rot.w:.4f}]"
            )

        except TransformException as ex:
            # 5. 捕获 tf2 查找失败的异常
            # 这里的行为模拟了原代码的 "except: continue"
            # self.get_logger().warn(f"Could not transform: {ex}")
            pass # 静默失败，继续等待

def main(args=None):
    rclpy.init(args=args)
    
    node = StaticTfListener()
    
    # rclpy.spin() 运行节点的所有回调（包括定时器）直到程序关闭
    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()