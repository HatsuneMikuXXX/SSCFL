from SSCFL import FacilityLocation
from local_search import initial_solution

FL = FacilityLocation(300, 300)
FL.set_demands_randomly([2,3,4], [0.2, 0.7, 0.1])
FL.set_capacities_randomly([7,12], [0.3, 0.7])
FL.set_facility_costs_randomly([20], [1])
FL.set_route_costs_randomly([1,2.5], [], discrete = False)
FL.set_preferences_randomly([1/300 for x in range(300)])

X = initial_solution(FL)
FL.status(print_issues = False)
