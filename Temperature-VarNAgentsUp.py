# coding: utf-8

# Imports
from __future__ import division
import matplotlib.pyplot as plt
from scipy import special

# Computing theoretical solution for the variance (numerically computed)
probabilities_eq1 = [2 * 0.5**1000 * special.binom(1000, x) for x in range(0, 500)]
mid_probability = 2 * 0.5**1000 * special.binom(1000, 500)
probabilities_eq2 = [2 * 0.5**1000 * special.binom(1000, x) for x in range(501, 1001)]
av_n_eq1 = sum(p*x for x, p in zip(range(0, 500), probabilities_eq1)) + mid_probability * 500 / 2
av_n_eq2 = sum(p*x for x, p in zip(range(501, 1001), probabilities_eq2)) + mid_probability * 500 / 2
av_n2_eq1 = sum(p*x**2 for x, p in zip(range(0, 500), probabilities_eq1)) + mid_probability * 500**2 / 2
av_n2_eq2 = sum(p*x**2 for x, p in zip(range(501, 1001), probabilities_eq2)) + mid_probability * 500**2 / 2
var_n_eq1 = av_n2_eq1 - av_n_eq1**2
var_n_eq2 = av_n2_eq2 - av_n_eq2**2

# Reading model results from file
temperatures = []
avNAgentsUp = []
varNAgentsUp = []
with open("./Results/Summary-Temperature-AltVarNAgentsUp.csv", "r") as f:
    for line in f:
        temperatures.append(float(line.split(",")[0]))
        avNAgentsUp.append(float(line.split(",")[1]))
        varNAgentsUp.append(float(line.split(",")[2]))

# Plot
fig = plt.figure(figsize=(8, 6), facecolor='white')
plt.plot(temperatures, varNAgentsUp, label="ABM")
plt.axhline(y=(var_n_eq1 + var_n_eq2) / 2, ls="--", c="r", label="Full noise prediction")
plt.yscale("log")
# plt.xlim(1.0, 14.0)
# plt.ylim(0.0, 1.0)
plt.ylabel("Variance of nAgentsUp (for individual equilibria)")
plt.xlabel("Temperature")
plt.legend()
plt.tight_layout()
# plt.savefig("./Temperature-AltVarNAgentsUp.pdf", format="pdf", dpi=300, bbox_inches='tight')

# Show
plt.show()
