import rosbag
import cv2
import sys
import os
import numpy as np
from Cryptodome.Cipher import AES
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import datetime
from multiprocessing import Process

# python3 compressed_img_bag_to_image.py PATH_TO_BAGFILE PATH_TO_OUTPUT_DIR NAME_OF_TARGET_TOPIC OUTPUT_SUFFIC[png|jpg]
# python3 compressed_img_bag_to_image.py ./2020-07-11-15-51-36.bag ./right /camera/right/image_color/compressed png



def unix2datetime(unix_time):
    date_time = datetime.datetime.fromtimestamp(unix_time) + datetime.timedelta(hours=9)
    return date_time.strftime("%Y-%m-%dT%H.%M.%S.%f")

# arguments
bag_path = sys.argv[1]
output_dir = sys.argv[2]
target_topic = sys.argv[3]
output_suffix = sys.argv[4]

if output_suffix != "jpg" and output_suffix != "png":
    raise ValueError("You should choose image format to output to jpg or png")

# load bag file
bag = rosbag.Bag(bag_path).read_messages()
print("bag file loaded!")

def write_msg_image(msg, t):
    # convert compressed image to cv image array
    np_array = np.frombuffer(msg.data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (819, 600))
    date_time = unix2datetime(t.to_sec())
    output_path = os.path.join(output_dir, date_time+"."+output_suffix)

    # output the image
    cv2.imwrite(output_path, image)
    
def multi_write_msg_image(buff_list):
    for msg, t in buff_list:
    	write_msg_image(msg, t)

process_list = []
buff = []

# loop in each message
for topic, msg, t in bag:
    if topic==target_topic:
        buff.append((msg, t))
        if len(buff) == 16:
            process = Process(
	            target=multi_write_msg_image,
	            kwargs={'buff_list': buff})
            process.start()
            process_list.append(process)
            buff = []

for process in process_list:
    process.join()
