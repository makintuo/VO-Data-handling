import os
import sys
from bisect import bisect_left
import shutil

left_times_path = sys.argv[1]
left_files = sys.argv[2]            
right_times_path = sys.argv[3]
right_files = sys.argv[4]   
new_left = sys.argv[5]
new_right = sys.argv[6]
parent_directory = sys.argv[7]

if not os.path.exists(new_left):
    os.mkdir(new_left)
if not os.path.exists(new_right):
    os.mkdir(new_right)

    
f = open(parent_directory + "/times.txt", "w")       
    
left_times = open(left_times_path, "r")
left = left_times.readlines()
left = [int(i) for i in left]

right_times = open(right_times_path, "r")
right = right_times.readlines()
right = [int(i) for i in right]

def take_closest(myList, myNumber):
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before

if len(right) > len(left):
    for timestamp in left:
        closest = take_closest(right, int(timestamp))
        if abs(int(timestamp) - int(closest)) <= 150000000:
            shutil.move(os.path.join(right_files, str(closest) + ".png"), os.path.join(new_right, str(timestamp).strip() + ".png"))
            shutil.move(os.path.join(left_files, str(timestamp) + ".png"), os.path.join(new_left, str(timestamp).strip() + ".png"))
            right.remove(closest)

else:
    for timestamp in right:
        closest = take_closest(left, int(timestamp))
        if abs(int(timestamp) - int(closest)) <= 150000000:
            shutil.move(os.path.join(left_files, str(closest) + ".png"), os.path.join(new_left, str(timestamp).strip() + ".png"))
            shutil.move(os.path.join(right_files, str(timestamp) + ".png"), os.path.join(new_right, str(timestamp).strip() + ".png"))
            left.remove(closest)


for path,dirs,files in os.walk(new_left):
    for filename in files:
        f.write(str(filename).strip(".png") + "\n")

f.close()
left_times.close()
right_times.close()
