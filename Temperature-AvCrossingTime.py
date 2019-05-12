# coding: utf-8

# Imports
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np


# Control variables
temperatures = np.linspace(0.23, 0.27, 41, endpoint=True)  # List of temperatures to simulate

# Reading model results from file
avCrossingTimes = []
stdCrossingTimes = []
for temperature in temperatures:
    with open("./Results/CrossingTimes-T{:.4f}.csv".format(temperature), 'r') as f:
        sumCrossingTimes = 0.0
        sumCrossingTimes2 = 0.0
        nCrossingTimes = 0
        for line in f:
            time_events = [int(x) for x in line.split(",")]
            for time1, time2 in zip(time_events[:-1], time_events[1:]):
                sumCrossingTimes += time2 - time1
                sumCrossingTimes2 += (time2 - time1)**2
                nCrossingTimes += 1
    avCrossingTimes.append(sumCrossingTimes/nCrossingTimes)
    stdCrossingTimes.append(np.sqrt(sumCrossingTimes2/nCrossingTimes - (sumCrossingTimes/nCrossingTimes)**2))

# Plot
fig = plt.figure(figsize=(8, 6), facecolor='white')
plt.errorbar(temperatures, avCrossingTimes, yerr=stdCrossingTimes, capsize=5, fmt="o-")
plt.yscale("log")
# plt.xlim(1.0, 14.0)
# plt.ylim(0.0, 1.0)
plt.ylabel("Av. Crossing Time")
plt.xlabel("Temperature")
# plt.legend()
plt.tight_layout()
# plt.savefig("./Temperature-AvCrossingTime.eps", format='eps', dpi=300, bbox_inches='tight')

# Show
plt.show()
