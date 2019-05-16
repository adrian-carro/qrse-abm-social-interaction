# coding: utf-8

# Imports
from __future__ import division
import numpy as np


# Control variables
# temperatures = np.linspace(0.23, 0.27, 41, endpoint=True)  # List of temperatures to simulate
temperatures = np.concatenate((np.linspace(0.1, 0.23, 13, endpoint=False), np.linspace(0.23, 0.27, 40, endpoint=False),
                               np.linspace(0.27, 0.9, 64, endpoint=True)), 0)
# temperatures = [0.5]
nAgents = 1000

# Reading model results from file
avNAgentsUp_eq1 = []
avNAgentsUp_eq2 = []
avNAgentsUp_weighted = []
varNAgentsUp_eq1 = []
varNAgentsUp_eq2 = []
varNAgentsUp_weighted = []
for temperature in temperatures:
    sum_n_eq1 = 0
    sum_n_eq2 = 0
    sum_n2_eq1 = 0
    sum_n2_eq2 = 0
    n_elements_eq1 = 0
    n_elements_eq2 = 0
    # Read crossing times
    time_events = []
    nAgentsUp = []
    prev_i = 0
    with open("./Results/CrossingTimes-T{:.4f}.csv".format(temperature), 'r') as f:
        for line in f:
            time_events.append([int(x) for x in line.split(",")])
            nAgentsUp.append([])
    if 0.23 <= temperature < 0.2350:
        with open("./Results/CrossingTimesB-T{:.4f}.csv".format(temperature), 'r') as f:
            for line in f:
                time_events.append([int(x) for x in line.split(",")])
                nAgentsUp.append([])
    # Read and temporarily store all realizations
    with open("./Results/nAgentsUp-T{:.4f}.csv".format(temperature), 'r') as f:
        for line in f:
            i = 0
            for element in line.split(","):
                nAgentsUp[i].append(int(element))
                i += 1
            prev_i = i
    if 0.23 <= temperature < 0.2350:
        with open("./Results/nAgentsUpB-T{:.4f}.csv".format(temperature), 'r') as f:
            for line in f:
                i = prev_i
                for element in line.split(","):
                    nAgentsUp[i].append(int(element))
                    i += 1
    # Add final time to time events
    i = 0
    for time_events_ts in time_events:
        time_events_ts.append(len(nAgentsUp[i]))
        i += 1
    # For each realization...
    for nAgentsUp_ts, time_events_ts in zip(nAgentsUp, time_events):
        # ...for each chunk...
        for initial_time, final_time in zip(time_events_ts[:-1], time_events_ts[1:]):
            chunk = nAgentsUp_ts[initial_time:final_time]
            # ...add elements to correct equilibrium
            if np.mean(chunk)/nAgents > 0.5:
                sum_n_eq1 += sum(chunk)
                sum_n2_eq1 += sum([x**2 for x in chunk])
                n_elements_eq1 += len(chunk)
            else:
                sum_n_eq2 += sum(chunk)
                sum_n2_eq2 += sum([x**2 for x in chunk])
                n_elements_eq2 += len(chunk)
    avNAgentsUp_eq1.append(sum_n_eq1 / n_elements_eq1)
    avNAgentsUp_eq2.append(sum_n_eq2 / n_elements_eq2)
    avNAgentsUp_weighted.append((avNAgentsUp_eq1[-1] * n_elements_eq1 + avNAgentsUp_eq2[-1] * n_elements_eq2)
                                / (n_elements_eq1 + n_elements_eq2))
    varNAgentsUp_eq1.append(sum_n2_eq1 / n_elements_eq1 - (sum_n_eq1 / n_elements_eq1)**2)
    varNAgentsUp_eq2.append(sum_n2_eq2 / n_elements_eq2 - (sum_n_eq2 / n_elements_eq2)**2)
    varNAgentsUp_weighted.append((varNAgentsUp_eq1[-1] * n_elements_eq1 + varNAgentsUp_eq2[-1] * n_elements_eq2)
                                 / (n_elements_eq1 + n_elements_eq2))
    print("T={} done".format(temperature))

# Write summary results to file
with open("./Results/Summary-Temperature-AltVarNAgentsUp.csv", "w") as f:
    for temperature, avNAgentsUp_element, varNAgentsUp_element in zip(temperatures, avNAgentsUp_weighted,
                                                                      varNAgentsUp_weighted):
        f.write("{}, {}, {}\n".format(temperature, avNAgentsUp_element, varNAgentsUp_element))
