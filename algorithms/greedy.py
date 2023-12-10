from SSCFLSO_validator import FL_Validator
from algorithms.preprocess import preprocess

def greedy(instance):
	possible_facilities = preprocess(instance)
	FLV = FL_Validator(instance)
	open_facilities = []
	FLV.set_solution(open_facilities)
	while not FLV.feasible() and set(open_facilities) != set(possible_facilities):
		closed_facilities = set(possible_facilities) - set(open_facilities)
		choices = []
		for facility in closed_facilities:
			FLV.set_solution(open_facilities + [facility])
			choices.append((facility, FLV.get_value()))
		choices.sort(key = lambda x: x[1])
		open_facilities.append(choices[0][0])
		FLV.set_solution(open_facilities)
	return open_facilities