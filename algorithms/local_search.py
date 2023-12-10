from SSCFLSO_validator import FL_Validator
from algorithms.preprocess import preprocess

categories = ["ADD", "REMOVE", "SWITCH"]

def local_search(instance):
	possible_facilities = preprocess(instance)
	FLV = FL_Validator(instance)
	FLV.set_solution(possible_facilities)
	# Remove open facilities that serve no one
	assignment = FLV.get_assignment()
	open_facilities = [j for j in possible_facilities if j in assignment.values()]
	FLV.set_solution(open_facilities)
	min_value = FLV.get_value()
	stuck_in_optima = False
	while not stuck_in_optima:
		stuck_in_optima = True
		for category in categories:
			N = get_neighborhood(open_facilities, possible_facilities, category)
			for next in N:
				FLV.set_solution(next)
				value = FLV.get_value()
				if FLV.feasible() and value < min_value:
					print("Could", category)
					print("New solution", next)
					open_facilities = next.copy()
					min_value = value
					stuck_in_optima = False
					break
			else:
				print("Current solution", open_facilities)
				print("Cannot", category)
				continue
			break
	return open_facilities

def get_neighborhood(open_facilities, possible_facilities, category):
	match category:
		case "ADD":
			return [open_facilities + [j] for j in possible_facilities if j not in open_facilities]
		case "REMOVE":
			return [open_facilities[:index] + open_facilities[index+1:] for index in range(len(open_facilities))]
		case "SWITCH":
			N = []
			closed_facilities = list(set(possible_facilities) - set(open_facilities))
			for j_remove in open_facilities:
				for j_add in closed_facilities:
					S = open_facilities.copy()
					S.remove(j_remove)
					S.append(j_add)
					N.append(S)
			return N
		case _:
			return []

        
