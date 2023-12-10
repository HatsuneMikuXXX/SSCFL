from SSCFLSO_generator import FL_Generator
from SSCFLSO_validator import FL_Validator
from random_helper import uniform
from preprocess import initial_solution


m = 3
n = 5
x = FL_Generator(m, n)
x.i300("instances/own_generated/test2.plc")
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

