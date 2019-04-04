# coding: utf-8

# Imports
from __future__ import division
import numpy as np
import random as rand

# Control variables
temperature = 5.0
mu = 3.0
numberOfAgents = 10
initialFraction = 0.5
randomNumbersSeed = 1

# Set seed for random number generator
rand.seed(randomNumbersSeed)

# Compute initial state of the system
state = []
nAgentsUp = 0
for i in range(numberOfAgents):
    if rand.random() <= initialFraction:
        state.append(1)
        nAgentsUp += 1
    else:
        state.append(0)

# Frequency of buying for a given agent
frequency = 1/(1 + np.exp(-(mu - nAgentsUp/numberOfAgents)/temperature))

print(frequency)
