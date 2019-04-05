# coding: utf-8

# Imports
from __future__ import division
import numpy as np
import random as rand
import matplotlib.pyplot as plt


def main():
    # Control variables
    temperature = 0.24
    mu = 0.5
    n_agents = 1000
    final_time = 10000
    initial_frequency = 0.5
    random_numbers_seed = 1
    control_plot_results = True
    control_write_results = False

    # Set seed for random number generator
    rand.seed(random_numbers_seed)

    # Run model
    ts_n_agents_up = social_interaction_model(temperature, mu, n_agents, final_time, initial_frequency)

    # Print results to file
    if control_write_results:
        write_results(temperature, ts_n_agents_up, "nAgentsUp")

    # Plot results
    if control_plot_results:
        print("hello")
        plot_results(final_time, n_agents, ts_n_agents_up, "nAgentsUp")


def social_interaction_model(temperature, mu, n_agents, final_time, initial_frequency):
    # Compute initial state of the system
    state = []
    n_agents_up = 0
    ts_n_agents_up = []
    for i in range(n_agents):
        if rand.random() <= initial_frequency:
            state.append(1)
            n_agents_up += 1
        else:
            state.append(0)
    # Store initial state in time series
    ts_n_agents_up.append(n_agents_up)

    # Start simulation
    t = 1
    while t <= final_time:
        # Update the frequency of buying for a given agent (for now, all agents have the same frequency)
        frequency = 1/(1 + np.exp((mu - n_agents_up / n_agents) / temperature))
        n_agents_up = 0
        for i, s in enumerate(state):
            # Synchronous update: all agents update their state at the same time, thus not being aware of the changes
            # of the other agents till next time step. TODO: Confirm this point with Jangho.
            if rand.random() <= frequency:
                state[i] = 1
                n_agents_up += 1
            else:
                state[i] = 0
        # Store current state in time series
        ts_n_agents_up.append(n_agents_up)
        t += 1
    return ts_n_agents_up


def write_results(temperature, time_series, file_name):
    """Prints results to file"""
    with open("./Results/" + file_name + "-T" + str(temperature) + ".csv", 'w') as f:
        for n in time_series[:-1]:
            f.write(str(n) + "\n")
        f.write(str(time_series[-1]))


def plot_results(final_time, n_agents, time_series, label):
    """Performs basic plotting"""
    plt.figure(figsize=(8, 6), facecolor='white')
    plt.plot(range(final_time + 1), time_series, "o-", label=label)
    plt.xlim(0.0, final_time)
    plt.ylim(0.0, n_agents)
    plt.ylabel("nAgentsUp")
    plt.xlabel("Time")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
