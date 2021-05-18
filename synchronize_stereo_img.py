import numpy as np
import os
import sys
from bisect import bisect_left
from shutil import copyfile

# python3 compare.py /home/kamijolab/Downloads/202007/times.txt /home/kamijolab/Downloads/202007/source_times.txt /home/kamijolab/Downloads/202007/left /home/kamijolab/Downloads/202007/new


times_path = sys.argv[1]
source_times = sys.argv[2]
source_path = sys.argv[3]
output_path = sys.argv[4]

if not os.path.exists(output_path):
    os.mkdir(output_path)

times = open(times_path, "r")
source_times = open(source_times, "r")

source = source_times.readlines()
source = [int(i) for i in source]

def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
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

for timestamp in times:
    closest = take_closest(source, int(timestamp))
    copyfile(os.path.join(source_path, str(closest) + ".png"), os.path.join(output_path, str(timestamp).strip() + ".png"))



times.close()
source_times.close()
