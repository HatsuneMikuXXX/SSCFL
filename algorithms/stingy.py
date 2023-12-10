from SSCFLSO_validator import FL_Validator
from algorithms.preprocess import preprocess

def stingy(instance):
	possible_facilities = preprocess(instance)
	FLV = FL_Validator(instance)
	FLV.set_solution(possible_facilities)
	# Remove open facilities that serve no one
	assignment = FLV.get_assignment()
	open_facilities = [j for j in possible_facilities if j in assignment.values()]

	FLV.set_solution(open_facilities)
	min_value = FLV.get_value()
	# Remove facility that introduce the most expensive costs (opening and travel)
	while True:
		choices = []
		for facility in open_facilities:
			tmp = open_facilities.copy()
			tmp.remove(facility)
			FLV.set_solution(tmp)
			if FLV.feasible():
				choices.append((facility, FLV.get_value()))
		choices.sort(key = lambda x: x[1])
		if choices == [] or choices[0][1] > min_value:
			break
		open_facilities.remove(choices[0][0])
		FLV.set_solution(open_facilities)
		min_value = FLV.get_value()
	return open_facilities