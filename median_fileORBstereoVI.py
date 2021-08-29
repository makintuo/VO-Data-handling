import numpy as np
import sys
import csv
import os
from datetime import datetime

files = []
    
dataset_path = str(sys.argv[1]).split("/")
   
for i in range(1, int(sys.argv[2])+1):
    f = '/home/kamijolab/Dev/ORB_SLAM3v0.4/Trajectories/' + dataset_path[4] + '/' + dataset_path[5] + "_" + str(i) + ".txt"
    if os.path.exists(f):
        a = np.genfromtxt(f, dtype=float)
        files.append(a.copy())

sizes = [a.shape[0] for a in files]

full_files = []

for a in files:
    if (a.shape[0] == max(sizes)):
        full_files.append(a.copy())

#average = (sum(files)) / float(sys.argv[3])
d = np.stack(full_files)
median = np.median(d, axis = 0)
#np.savetxt('/home/kamijolab/Dev/ORB_SLAM3v0.4/Trajectories/' + dataset_path[4] + '/' + dataset_path[5] + '_VImedian' + str(len(full_files)) + "_" + datetime.today().strftime('%Y-%m-%d') + '.txt', median, delimiter=' ')

with open('/home/kamijolab/Dev/ORB_SLAM3v0.4/Trajectories/' + dataset_path[4] + '/' + dataset_path[5] + '_VImedian' + str(len(full_files)) + "_" + datetime.today().strftime('%Y-%m-%d_%H:%M') + '.csv', 'w') as txt:
    csv.writer(txt, delimiter=' ').writerows(median)

print("Median trajectory created from " + str(len(full_files)) + " trajectories.\n" + dataset_path[5] + '_VImedian' + str(len(full_files)) + "_" + datetime.today().strftime('%Y-%m-%d_%H:%M') + '.csv')


for i in range(1, int(sys.argv[2])+1):
    f = '/home/kamijolab/Dev/ORB_SLAM3v0.4/Trajectories/' + dataset_path[4] + '/' + dataset_path[5] + "_" + str(i) + ".txt"
    if os.path.exists(f):
        os.remove(f)
    else:
        print("The file does not exist")
        
print("Source files removed")

txt.close()
