# coding: utf-8

# Imports
from __future__ import division
import matplotlib.pyplot as plt


# Reading model results from file
nAgentsUp = []
with open("./Results/nAgentsUp-T0.1.csv", 'r') as f:
    for line in f:
        nAgentsUp.append(float(line))

# Plot
fig = plt.figure(figsize=(8, 6), facecolor='white')
plt.plot(range(len(nAgentsUp)), nAgentsUp, "o-", label="nAgentsUp")
# plt.xlim(0.0, len(nAgentsUp))
plt.xlim(0.0, 100)
plt.ylim(0.0, 1000)
plt.ylabel("nAgentsUp")
plt.xlabel("Time")
# plt.legend()
plt.tight_layout()
# plt.savefig('./EmploymentIncomeDist.eps', format='eps', dpi=300, bbox_inches='tight')
# plt.savefig('./EmploymentIncomeDist.pdf', format='pdf', dpi=300, bbox_inches='tight')

# Show
plt.show()