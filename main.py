from SSCFLSO_generator import FL_Generator
from SSCFLSO_validator import FL_Validator
from random_helper import uniform
from algorithms.preprocess import preprocess
from algorithms.greedy import greedy
from algorithms.stingy import stingy
from algorithms.brute_force import brute_force
from algorithms.local_search import local_search


i = FL_Generator.load_instance("instances/own_generated/example.plc")
x = FL_Validator(i)
brute_force(i, show_all_feasible=True)
o = local_search(i)
print(o)
x.set_solution(o)
print(x.get_value())



#str_to_dict(s)
#for key, value in d.items():
#    print(key, value)

#x.i300()
#(a,b,c,d,e,f,g) = x.get_instance()

#o = initial_solution(x)

#y = FL_Validator(a,b,c,d,e,f,g)
#y.set_solution(o)
#print(o)
#print(y.feasible())
#print(y.get_value())

