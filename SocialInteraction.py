# coding: utf-8

# Imports
from __future__ import division
import numpy as np
import random as rand
import matplotlib.pyplot as plt

# Control variables
temperature = 0.24
mu = 0.5
nAgents = 1000
finalTime = 10000
initialFrequency = 0.5
randomNumbersSeed = 1
plotResults = True
writeResults = False

# Set seed for random number generator
rand.seed(randomNumbersSeed)

# Compute initial state of the system
state = []
nAgentsUp = 0
ts_nAgentsUp = []
for i in range(nAgents):
    if rand.random() <= initialFrequency:
        state.append(1)
        nAgentsUp += 1
    else:
        state.append(0)
# Store initial state in time series
ts_nAgentsUp.append(nAgentsUp)

# Start simulation
t = 1
while t <= finalTime:
    # Update the frequency of buying for a given agent (for now, all agents have the same frequency)
    frequency = 1/(1 + np.exp((mu - nAgentsUp / nAgents) / temperature))
    nAgentsUp = 0
    for i, s in enumerate(state):
        # Synchronous update: all agents update their state at the same time, thus not being aware of the changes of the
        # other agents till next time step. TODO: Confirm this point with Jangho.
        if rand.random() <= frequency:
            state[i] = 1
            nAgentsUp += 1
        else:
            state[i] = 0
    # Store current state in time series
    ts_nAgentsUp.append(nAgentsUp)
    t += 1

# Print results to file
if writeResults:
    with open("./Results/nAgentsUp-T" + str(temperature) + ".csv", 'w') as f:
        for n in ts_nAgentsUp[:-1]:
            f.write(str(n) + "\n")
        f.write(str(ts_nAgentsUp[-1]))

# Plot results
if plotResults:
    fig = plt.figure(figsize=(8, 6), facecolor='white')
    plt.plot(range(finalTime + 1), ts_nAgentsUp, "o-", label="nAgentsUp")
    plt.xlim(0.0, finalTime)
    plt.ylim(0.0, nAgents)
    plt.ylabel("nAgentsUp")
    plt.xlabel("Time")
    plt.tight_layout()
    plt.show()
