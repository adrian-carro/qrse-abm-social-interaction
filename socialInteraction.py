# coding: utf-8

# Imports
from __future__ import division
import numpy as np
import random as rand

# Control variables
temperature = 1.0
mu = 0.5
nAgents = 1000
finalTime = 10000
initialFrequency = 0.5
randomNumbersSeed = 1

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
    frequency = 1/(1 + np.exp(-(mu - nAgentsUp / nAgents) / temperature))
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
with open("./Results/nAgentsUp-T" + str(temperature) + ".csv", 'w') as f:
    for n in ts_nAgentsUp[:-1]:
        f.write(str(n) + "\n")
    f.write(str(ts_nAgentsUp[-1]))
