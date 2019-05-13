# coding: utf-8

# Imports
from __future__ import division
import numpy as np


# Control variables
temperatures = np.linspace(0.23, 0.27, 41, endpoint=True)  # List of temperatures to simulate

# Reading model results from file
avNAgentsUp = []
varNAgentsUp = []
for temperature in temperatures:
    sumNAgentsUp = 0.0
    sumNAgentsUp2 = 0.0
    n = 0
    with open("./Results/nAgentsUp-T{:.4f}.csv".format(temperature), 'r') as f:
        for line in f:
            for element in line.split(","):
                sumNAgentsUp += int(element)
                sumNAgentsUp2 += int(element) ** 2
                n += 1
    if temperature < 0.2350:
        with open("./Results/nAgentsUpB-T{:.4f}.csv".format(temperature), 'r') as f:
            for line in f:
                for element in line.split(","):
                    sumNAgentsUp += int(element)
                    sumNAgentsUp2 += int(element) ** 2
                    n += 1
    avNAgentsUp.append(sumNAgentsUp/n)
    varNAgentsUp.append(sumNAgentsUp2/n - (sumNAgentsUp/n)**2)

# Write summary results to file
with open("./Results/Summary-Temperature-VarNAgentsUp.csv", "w") as f:
    for temperature, avNAgentsUp_element, varNAgentsUp_element in zip(temperatures, avNAgentsUp, varNAgentsUp):
        f.write("{}, {}, {}\n".format(temperature, avNAgentsUp_element, varNAgentsUp_element))
