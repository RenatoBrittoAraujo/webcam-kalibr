import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import os

rospy.init_node("image_publisher")
pub = rospy.Publisher("/camera/image_raw", Image, queue_size=10)
bridge = CvBridge()

image_folder = "images"
image_files = [f for f in os.listdir(image_folder) if f.endswith(".png")]
print(f"found {len(image_files)} images")

rate = rospy.Rate(10)  # Hz
for i, image_file in enumerate(image_files):
    img = cv2.imread(os.path.join(image_folder, image_file))
    msg = bridge.cv2_to_imgmsg(img, encoding="bgr8")
    pub.publish(msg)
    rate.sleep()
    print(f"published image {i+1}/{len(image_files)}")
