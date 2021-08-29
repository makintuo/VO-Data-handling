#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import cv2

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

bag_path = sys.argv[1]
output_path = sys.argv[2]
folder = sys.argv[3]
topic_path = "/camera/" + str(folder) + "/image_color/compressed"

print("Extract images from %s on topic %s into %s" % (bag_path, topic_path, output_path))                                                  
                                                      
if not os.path.exists(output_path):
    os.mkdir(output_path)
if not os.path.exists(os.path.join(output_path, str(folder))):
    os.mkdir(os.path.join(output_path, str(folder)))
    
f = open(os.path.join(output_path, str(folder) + "times.txt"), "w")   

bag = rosbag.Bag(bag_path, "r")
bridge = CvBridge()

for topic, msg, t in bag.read_messages(topics=[topic_path]):
    cv_img = bridge.compressed_imgmsg_to_cv2(msg)
    cv_img = cv2.resize(cv_img, (819, 600))

    h = msg.header.stamp
    #cv2.imwrite(os.path.join(args.output_dir, "%s_(%s).png" % (time_str, seconds)), cv_img)
    cv2.imwrite(os.path.join(output_path, folder, "%s.png" % (h)), cv_img)

count = 0

for path,dirs,files in os.walk(os.path.join(output_path, str(folder))):
    for filename in files:
        f.write(str(filename).strip(".png") + "\n")
        count += 1
        
print("Number of images in folder '%s': %s" % (folder, count))

bag.close()
f.close()
