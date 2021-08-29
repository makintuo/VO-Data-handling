import os
import sys
for i in range(1, len(sys.argv)):
    source = open(os.path.join(sys.argv[i], "state_groundtruth_estimate0/data.csv"), "r")
    destination = open(os.path.join(sys.argv[i], "state_groundtruth_estimate0/GroundTruth.txt"), "w")
    next(source)

    for line in source:
        array = line.split(",")
        destination.write("%s %s %s %s %s %s %s %s\n" % (array[0], array[1], array[2], array[3], array[4], array[5], array[6], array[7]))

    source.close()
    destination.close()
