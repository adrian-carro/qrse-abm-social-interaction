# coding: utf-8

# Imports
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np


# Control variables
temperature = 0.235

# Reading model results from file
times = []
with open("./Results/CrossingTimes-T{:.4f}.csv".format(temperature), 'r') as f:
    for line in f:
        time_events = [int(x) for x in line.split(",")]
        for time1, time2 in zip(time_events[:-1], time_events[1:]):
            times.append(np.log(time2 - time1))

# Creating bins for the histogram
myBins = np.linspace(0.0, 14.0, 29, endpoint=True)

# Plot
fig = plt.figure(figsize=(8, 6), facecolor='white')
plt.hist(times, bins=myBins, density=True)
plt.xlim(0.0, 14.0)
# plt.ylim(0.0, 1.0)
plt.ylabel("Prob. Density")
plt.xlabel("Crossing times")
plt.title("T = {:.4f}".format(temperature))
# plt.legend()
plt.tight_layout()
# plt.savefig("./CrossingTimesProbDist-T{:.4f}.eps".format(temperature), format='eps', dpi=300, bbox_inches='tight')

# Show
plt.show()
