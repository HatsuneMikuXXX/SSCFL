from SSCFLSO_generator import FL_Generator
from SSCFLSO_validator import FL_Validator
from random_helper import uniform
from algorithms.preprocess import preprocess
from algorithms.greedy import greedy
from algorithms.stingy import stingy
from algorithms.brute_force import brute_force
from algorithms.local_search import local_search
from run import run


s = "instances/i300/i300_"
filenames = []
for i in range(1, 21):
	t = s
	t += str(i) + ".plc"
	filenames.append(t)
save_location = "experimental_results/i300_Greedy.txt"
run(filenames, save_location, no_preferences_included=True)
