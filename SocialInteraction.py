# coding: utf-8

# Imports
from __future__ import division
import numpy as np
import random as rand
import matplotlib.pyplot as plt
import scipy.optimize as optimize


def main():
    # Control variables
    # temperatures = np.linspace(0.2, 0.3, 41, endpoint=True)  # List of temperatures to simulate
    temperatures = [0.27]
    mu = 0.5
    n_agents = 1000
    final_time = 10000
    n_realizations = 1  # Realizations per temperature value
    initial_frequency = 0.5
    random_numbers_seed = 1
    control_write_time_series = False
    control_plot_time_series = False
    control_compute_passage_times = True

    # Confirm large number of plots with user
    check_control_variables(control_write_time_series, control_plot_time_series, control_compute_passage_times,
                            len(temperatures) * n_realizations)

    # # # # # # # # # # Time series # # # # # # # # # #
    if not control_compute_passage_times:
        # Iterate over temperatures and realizations
        i = 0
        for temperature in temperatures:
            ts_collector = []
            for realization in range(n_realizations):

                # Set seed for random number generator for this realization and temperature
                rand.seed(random_numbers_seed * i)

                # Run model
                ts_n_agents_up = social_interaction_model(temperature, mu, n_agents, final_time, initial_frequency)

                # If printing results to file, collect time series for a given temperature
                if control_write_time_series:
                    ts_collector.append(ts_n_agents_up)

                # Plot results
                if control_plot_time_series:
                    plot_time_series(final_time, n_agents, ts_n_agents_up, temperature)

                i += 1

            # Print results to file
            if control_write_time_series:
                write_time_series(temperature, ts_collector, "nAgentsUp")

        # So that plots are shown
        if control_plot_time_series:
            plt.show()

    # # # # # # # # # # Passage times # # # # # # # # # #
    else:
        # Iterate over temperatures and realizations
        i = 0
        for temperature in temperatures:
            ts_collector = []
            for realization in range(n_realizations):

                # Set seed for random number generator for this realization and temperature
                rand.seed(random_numbers_seed * i)

                # Find approximate analytical solution for the fixed points
                initial_guess = 0.0001  # Starting point for approximation (should be close enough to actual value)
                x1 = optimize.newton(func, initial_guess, fprime=func_prima, args=(temperature,), tol=1.5e-09,
                                     maxiter=50)
                x2 = 1 - x1

                # Run model
                ts_n_agents_up, crossing_times = social_interaction_model_with_crossing_times(temperature, mu, n_agents,
                                                                                              final_time,
                                                                                              initial_frequency,
                                                                                              x1 * n_agents,
                                                                                              x2 * n_agents)

                print(crossing_times)
                plot_time_series_with_crossing_times(final_time, n_agents, ts_n_agents_up, temperature, x1, x2,
                                                     crossing_times)
                plt.show()

        #         # If printing results to file, collect time series for a given temperature
        #         if control_write_time_series:
        #             ts_collector.append(crossing_times)
        #
        #         # Plot results
        #         if control_plot_time_series:
        #             plot_results(final_time, n_agents, crossing_times, temperature)
        #
        #         i += 1
        #
        #     # Print results to file
        #     if control_write_time_series:
        #         write_results(temperature, ts_collector, "nAgentsUp")
        #
        # # So that plots are shown
        # if control_plot_time_series:
        #     plt.show()


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


def social_interaction_model_with_crossing_times(temperature, mu, n_agents, final_time, initial_frequency, x1, x2):
    # Compute initial state of the system
    state = []
    n_agents_up = 0
    ts_n_agents_up = []
    crossing_times = []
    for i in range(n_agents):
        if rand.random() <= initial_frequency:
            state.append(1)
            n_agents_up += 1
        else:
            state.append(0)
    ts_n_agents_up.append(n_agents_up)
    # Store initial state as old state and set most recent equilibrium to None
    old_n_agents_up = n_agents_up
    most_recent_equilibrium = None

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
        # Check if any equilibrium line has been crossed and possibly store the time
        if old_n_agents_up < x1 < n_agents_up or old_n_agents_up > x1 > n_agents_up:
            if most_recent_equilibrium != 1:
                crossing_times.append(t)
                most_recent_equilibrium = 1
        if old_n_agents_up < x2 < n_agents_up or old_n_agents_up > x2 > n_agents_up:
            if most_recent_equilibrium != 2:
                crossing_times.append(t)
                most_recent_equilibrium = 2
        # Update old state with current state
        old_n_agents_up = n_agents_up
        ts_n_agents_up.append(n_agents_up)
        t += 1
    return ts_n_agents_up, crossing_times


def func(x, temperature):
    return x + temperature * (np.log(1 - x) - np.log(x)) - 1 / 2


def func_prima(x, temperature):
    return 1 - temperature / (x * (1 - x))


def write_time_series(temperature, time_series_collector, file_name):
    """Prints results to file"""
    with open("./Results/" + file_name + "-T{:.4f}.csv".format(temperature), 'w') as f:
        for i, line in enumerate(zip(*time_series_collector)):
            if i < len(time_series_collector[1]) - 1:
                f.write("%s\n" % ", ".join([str(element) for element in line]))
            else:
                f.write("%s" % ", ".join([str(element) for element in line]))


def plot_time_series(final_time, n_agents, time_series, temperature):
    """Performs basic plotting"""
    plt.figure(figsize=(8, 6), facecolor='white')
    plt.plot(range(final_time + 1), [x / n_agents for x in time_series], "o-")
    plt.xlim(0.0, final_time)
    plt.ylim(0.0, 1.0)
    plt.ylabel("nAgentsUp / nAgents")
    plt.xlabel("Time")
    plt.title("T = " + str(temperature))
    plt.tight_layout()
    plt.draw()


def plot_time_series_with_crossing_times(final_time, n_agents, time_series, temperature, x1, x2, crossing_times):
    """Performs basic plotting"""
    plt.figure(figsize=(8, 6), facecolor='white')
    plt.plot(range(final_time + 1), [x / n_agents for x in time_series], "o-")
    plt.axhline(y=x1, c="r")
    plt.axhline(y=x2, c="r")
    for crossing_time in crossing_times:
        plt.axvline(x=crossing_time, c="r")
    plt.xlim(0.0, final_time)
    plt.ylim(0.0, 1.0)
    plt.ylabel("nAgentsUp / nAgents")
    plt.xlabel("Time")
    plt.title("T = " + str(temperature))
    plt.tight_layout()
    plt.draw()


def check_control_variables(control_write_results, control_plot_results, control_compute_passage_times,
                            number_of_plots):
    """Checks that control parameter values make sense"""
    if not control_write_results and not control_plot_results and not control_compute_passage_times:
        print("Neither writing results nor plotting them!\n"
              "Aborting simulation.")
        exit()
    if control_plot_results and number_of_plots > 10:
        reply = raw_input("Are you sure you want to generate {} plots?\n"
                          "To confirm, type \"Y\": ".format(number_of_plots))
        if reply != "Y":
            print("Aborting simulation.")
            exit()
        else:
            print("Continuing simulation.")


if __name__ == "__main__":
    main()
