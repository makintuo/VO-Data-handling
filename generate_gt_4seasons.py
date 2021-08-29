import os
import sys

for i in range(1, len(sys.argv)):
    source = open(os.path.join(sys.argv[i], "GNSSPoses.txt"), "r")
    destination = open(os.path.join(sys.argv[i], "GroundTruth.txt"), "w")
    next(source)

    for line in source:
        array = line.split(",")
        for value in array[1:4]:
            array[array.index(value)] = float(value) * float(array[8])
        destination.write(array[0][:10] + "." + array[0][10:15] + " %.15f %.15f %.15f %s %s %s %s\n" % (array[1], array[2], array[3], array[4], array[5], array[6], array[7]))

    source.close()
    destination.close()
