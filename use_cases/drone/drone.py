import copy

import numpy as np
from matplotlib.patheffects import withStroke

np.random.seed(42)

from mitl import load_formula, evaluate_robustness_semantics, evaluate_boolean_semantics

formula = 'F[10,20](a & F[40,50] (b & F[20,30] c))'


def apply_perturbation(trajectory, delta):
    copy_trajectory = copy.deepcopy(trajectory)
    copy_trajectory[1] = (copy_trajectory[1][0] + np.random.normal(0, delta), copy_trajectory[1][1])
    copy_trajectory[2] = (copy_trajectory[2][0] + np.random.normal(0, delta), copy_trajectory[2][1])
    copy_trajectory[3] = (copy_trajectory[3][0] + np.random.normal(0, delta), copy_trajectory[3][1])
    return copy_trajectory


print("========================")
print("EXAMPLE OF PERTURBATION")
print("========================")
sigma = [(0, "start"), (15, {"a"}), (60, {"b"}), (85, {"c"})]
sigma_pert = apply_perturbation(sigma, 0.1)

# original trajectory
print("original trajectory")
print("------------------------")
robustness = evaluate_robustness_semantics(sigma, load_formula(formula))
print("sigma=", sigma)
print("formula=", formula)
print("robustness of sigma=", robustness)

# perturbed trajectory
print("------------------------")
print("perturbed trajectory")
print("------------------------")
robustness = evaluate_robustness_semantics(sigma_pert, load_formula(formula))
print("sigma_pert=", sigma_pert)
print("formula=", formula)
print("robustness of sigma_pert=", robustness)

############### ---------------------

print("------------------------")
print("TRAJECTORY sigma_a")
print("------------------------")
sigma_a = [(0, "start"), (15, {"a"}), (60, {"b"}), (85, {"c"})]
robustness = evaluate_robustness_semantics(sigma_a, load_formula(formula))
print("sigma_a=", sigma_a)
print("formula=", formula)
print("robustness of sigma_a=", robustness)

print("------------------------")
print("TRAJECTORY sigma_b")
print("------------------------")

sigma_b = [(0, "start"), (17, {"a"}), (61, {"b"}), (87, {"c"})]
robustness = evaluate_robustness_semantics(sigma_b, load_formula(formula))
print("sigma_b=", sigma_b)
print("formula=", formula)
print("robustness of sigma_b=", robustness)

print("------------------------")
print("TRAJECTORY sigma_c")
print("------------------------")
sigma_c = [(0, "start"), (13, {"a"}), (61, {"b"}), (90, {"c"})]
robustness = evaluate_robustness_semantics(sigma_c, load_formula(formula))
print("sigma_c=", sigma_c)
print("formula=", formula)
print("robustness of sigma=", robustness)
print(" ")

###- GENERATE TABLE OF USE CASE 1
perturbations = [0.1, 1, 2, 3, 4, 5, 6]
traces = [("sigma_a", sigma_a), ("sigma_b", sigma_b), ("sigma_c", sigma_c)]

print("TABLE OF USE CASE 1")
print("----------------------------------")
print("trajectory, pert, mean, std, prob")
print("----------------------------------")
for trace in traces:
    for perturbation in perturbations:
        perturbed_traces = [apply_perturbation(trace[1], perturbation) for _ in range(1000)]
        robustness_values = [evaluate_robustness_semantics(perturbed_trace, load_formula(formula)) for perturbed_trace
                             in
                             perturbed_traces]
        boolean_values = [evaluate_boolean_semantics(perturbed_trace, load_formula(formula)) for perturbed_trace in
                          perturbed_traces]
        print(trace[0], perturbation, np.mean(robustness_values), np.std(robustness_values), np.mean(boolean_values))
print("==== END OF TABLE ====")

###-
###- GENERATE FIGURE OF USE CASE 1
def apply_perturbation_with_sum(trajectory, delta):
    pert = [np.random.normal(0, delta) for _ in range(3)]
    copy_trajectory = copy.deepcopy(trajectory)
    copy_trajectory[1] = (copy_trajectory[1][0] + pert[0], copy_trajectory[1][1])
    copy_trajectory[2] = (copy_trajectory[2][0] + pert[1], copy_trajectory[2][1])
    copy_trajectory[3] = (copy_trajectory[3][0] + pert[2], copy_trajectory[3][1])
    return copy_trajectory, sum([abs(a) for a in pert])


sum_pert = []
rob_pert = []
boolean_pert = []
for _ in range(20000):
    trace, s = apply_perturbation_with_sum(sigma_b, 2.0)
    robustness = evaluate_robustness_semantics(trace, load_formula(formula))
    boolean_semantics = evaluate_boolean_semantics(trace, load_formula(formula))
    rob_pert.append(robustness)
    boolean_pert.append(boolean_semantics)
    sum_pert.append(s)

import matplotlib.pyplot as plt

plt.rcParams.update({
    'axes.labelsize': 14,  # axis labels
    'xtick.labelsize': 12,  # x-axis tick labels
    'ytick.labelsize': 12,  # y-axis tick labels
    'legend.fontsize': 10  # legend text
})

colors = np.where(boolean_pert, '#1f77b4', '#d62728')
plt.scatter(sum_pert, rob_pert, c = colors,  s=3)
plt.scatter(0, 3, color='k', s=60, marker='o', edgecolors='white', zorder=3, label='Point (0, 5)')
plt.text(-0.5, 2.5, r'$\sigma_b$', fontsize=10, color='k')

plt.axhline(y=0, color='k', linestyle='--', linewidth=1, label='y = 5')
plt.axvline(x=3, ymin=0, ymax=10, color='k', linestyle='--', linewidth=1, label='x = 5')
x_line = np.linspace(0, 12, 100)
y_line = -x_line + 3
plt.plot(x_line, y_line, color='k', linestyle='-', linewidth=2.5, label='y = -x + 3')
y_line = x_line + 3
plt.plot(x_line, y_line, color='k', linestyle='-', linewidth=2.5, label='y = x + 3')

outline = withStroke(linewidth=6, foreground="white")

plt.text(8,  -2, 'C', fontsize=30, color='k', path_effects=[outline])
plt.text(8, 3, 'B', fontsize=30, color='k',path_effects=[outline])
plt.text(2, 3, 'A', fontsize=30, color='k', path_effects=[outline])

plt.tight_layout()

plt.xlim(-1, 10)
plt.ylim(-7, 6)
plt.xlabel(r'$\ell^1$ perturbation')
plt.ylabel(r"robustness ($\rho$)")
plt.savefig("./results/figure.pdf", bbox_inches="tight")  # vector for journals
plt.savefig("./results/figure.png", dpi=600, bbox_inches="tight")  # high-res raster
plt.show()

###-