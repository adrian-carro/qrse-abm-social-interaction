# coding: utf-8

# Imports
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Control variables
temperatures = np.linspace(0.23, 0.27, 41, endpoint=True)  # List of temperatures to simulate
# statistic_to_use = "Mean"
# statistic_to_use = "Median"
# statistic_to_use = "ModeUnitBins"
statistic_to_use = "ModeLogBins"

# Creating bins for the histogram for computing the mode
bin_edges = np.linspace(0.0, 15.0, 31, endpoint=True)
bin_centers = (bin_edges[1:] + bin_edges[:-1])/2.0

# Reading model results from file
avCrossingTimes = []
stdCrossingTimes = []
for temperature in temperatures:
    crossingTimes = []
    with open("./Results/CrossingTimes-T{:.4f}.csv".format(temperature), 'r') as f:
        for line in f:
            time_events = [int(x) for x in line.split(",")]
            for time1, time2 in zip(time_events[:-1], time_events[1:]):
                crossingTimes.append(time2 - time1)
    if 0.23 <= temperature < 0.2350:
        with open("./Results/CrossingTimesB-T{:.4f}.csv".format(temperature), 'r') as f:
            for line in f:
                time_events = [int(x) for x in line.split(",")]
                for time1, time2 in zip(time_events[:-1], time_events[1:]):
                    crossingTimes.append(time2 - time1)
    if statistic_to_use == "Mean":
        avCrossingTimes.append(np.mean(crossingTimes))
    elif statistic_to_use == "Median":
        avCrossingTimes.append(np.median(crossingTimes))
    elif statistic_to_use == "ModeUnitBins":
        avCrossingTimes.append(stats.mode(crossingTimes)[0][0])
    elif statistic_to_use == "ModeLogBins":
        counts, bins = np.histogram([np.log(x) for x in crossingTimes], bins=bin_edges)
        avCrossingTimes.append(np.exp(bin_centers[np.argmax(counts)]))
    stdCrossingTimes.append(np.std(crossingTimes))

# Plot
fig = plt.figure(figsize=(8, 6), facecolor='white')
# plt.errorbar(temperatures, avCrossingTimes, yerr=stdCrossingTimes, capsize=5, fmt="o-")
plt.plot(temperatures, avCrossingTimes, "o-")
# plt.plot([1/x for x in temperatures], avCrossingTimes, "o-")
plt.yscale("log")
# plt.xscale("log")
# plt.xlim(1.0, 14.0)
# plt.ylim(0.0, 1.0)
plt.ylabel(statistic_to_use + " Crossing Time")
plt.xlabel("Temperature")
# plt.legend()
plt.tight_layout()
# plt.savefig("./Temperature-" + statistic_to_use + "CrossingTime.pdf", format="pdf", dpi=300, bbox_inches='tight')

# Show
plt.show()
