# coding: utf-8

# Imports
from __future__ import division
import matplotlib.pyplot as plt

# Reading model results from file
temperatures = []
avNAgentsUp = []
varNAgentsUp = []
with open("./Results/Summary-Temperature-VarNAgentsUp.csv", "r") as f:
    for line in f:
        temperatures.append(float(line.split(",")[0]))
        avNAgentsUp.append(float(line.split(",")[1]))
        varNAgentsUp.append(float(line.split(",")[2]))

# Plot
fig = plt.figure(figsize=(8, 6), facecolor='white')
plt.plot(temperatures, varNAgentsUp)
# plt.yscale("log")
# plt.xlim(1.0, 14.0)
# plt.ylim(0.0, 1.0)
plt.ylabel("Variance of nAgentsUp")
plt.xlabel("Temperature")
# plt.legend()
plt.tight_layout()
# plt.savefig("./Temperature-AvCrossingTime.eps", format='eps', dpi=300, bbox_inches='tight')

# Show
plt.show()
