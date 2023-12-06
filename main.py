from SSCFLSO_generator import FL_Generator
from SSCFLSO_validator import FL_Validator
from local_search import initial_solution

n = 300
m = 300
x = FL_Generator(n, m)
x.i300()
(a,b,c,d,e,f,g) = x.get_instance()

o = initial_solution(x)

y = FL_Validator(a,b,c,d,e,f,g)
y.set_solution(o)
print(o)
print(y.feasible())
print(y.get_value())

