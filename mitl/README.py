from mitl import load_formula, evaluate_robustness_semantics, evaluate_boolean_semantics

# Use of monitoring algorithm

trajectory = [(0, {"a"}), (4, {"a", "d"}), (8, {"z", "h"}), (12, {"a"}), (78, {"a"})]  # this is a trajectory

formula = 'F[5,9](z & G[10,34](a))'
loaded_formula = load_formula(formula)  # loading a formula

boolean_semantics = evaluate_boolean_semantics(trajectory, loaded_formula)
quantitative_semantics = evaluate_robustness_semantics(trajectory, loaded_formula)

print("Boolean semantics: ", boolean_semantics)
print("time robustness: ", quantitative_semantics)