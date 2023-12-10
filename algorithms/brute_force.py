from SSCFLSO_validator import FL_Validator
from algorithms.preprocess import preprocess
from data_helper import powerset

# WARNING: Only use one small instances. This is not an heuristic!!
def brute_force(instance, show_all_feasible = False):
	possible_facilities = preprocess(instance)
	if len(possible_facilities) > 6:
		print("Too many facilities")
		return []

	FLV = FL_Validator(instance)
	open_facilities = []
	min_value = -1
	for combination in powerset(possible_facilities):
		FLV.set_solution(combination)
		value = FLV.get_value()
		feasible = FLV.feasible()
		if feasible and (value < min_value or min_value == -1):
			open_facilities = combination.copy()
			min_value = value
		if feasible and show_all_feasible:
			print(combination, value)
	return open_facilities

