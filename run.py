from time import time
from SSCFLSO_generator import FL_Generator
from SSCFLSO_validator import FL_Validator
from algorithms.local_search import local_search
from algorithms.greedy import greedy
from algorithms.stingy import stingy

algorithms = [greedy]
algorithm_names = ["G"]

# filenames = List of paths where instances are located
# save_location = where to store the algorithm, runtimes, solution, and solution value. Format Algo - Value - Runtime - Solution
# max_run_time, if positive restricts how long an algorithm may run
def run(filenames, save_location, max_run_time = -1, no_preferences_included = False, precision = 4):
	results = []
	n = len(algorithms)
	assert len(algorithm_names) == n
	print("Running tests. Preferences included in instances", not no_preferences_included)
	for index in range(n):
		algo = algorithms[index]
		print("Running", algorithm_names[index])
		for filename in filenames:
			print("Loading", filename)
			i = FL_Generator.load_instance(filename, no_preferences_included)
			validator = FL_Validator(i)
			start = time()
			solution = algo(i)
			end = time()
			runtime = round((end - start), precision) # measure in seconds
			validator.set_solution(solution)
			value = round(validator.get_value(), precision)
			results.append((algorithm_names[index], value, runtime, solution))
	
	# Writing results
	table = ""
	for (a,v,r,s) in results:
		table += a + ": " + str(v) + "\t" + str(r) + "s\t" + str(s) + "\n"
	file = open(save_location, 'w')
	file.write(table)
	file.close()
	return True