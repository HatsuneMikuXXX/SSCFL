from SSCFL import FacilityLocation
from local_search import initial_solution

FL = FacilityLocation(17, 5)
FL.set_demands_randomly([1,2,3], [0.2, 0.7, 0.1])
FL.set_capacities_randomly([15,17], [0.15, 0.85])
FL.set_facility_costs_randomly([20], [1])
FL.set_route_costs_randomly([1,2.5], [], discrete = False)
FL.set_prefereces_randomly([0.4, 0.2, 0.2, 0.1, 0.1])

X = initial_solution(FL)
FL.status(print_issues = False)
