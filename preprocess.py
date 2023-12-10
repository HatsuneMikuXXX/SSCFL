from SSCFLSO_validator import FL_Validator

# Preprocessing: Remove facilities that can never be opened

# Returns an initial solution using the stingy heuristic
def initial_solution(FL_Generator):
    (clients,facilities,demands,capacities,opening_cost,travel_cost,preferences) = FL_Generator.get_instance()
    FLV = FL_Validator(clients,facilities,demands,capacities,opening_cost,travel_cost,preferences)
    open_facilities = facilities
    FLV.set_solution(open_facilities)
    while bool(open_facilities) and not FLV.feasible():
        facilities_to_close = facilities_capacity_exceeded(demands,capacities, FLV.get_assignment())
        open_facilities = list(set(open_facilities) - set(facilities_to_close))
        FLV.set_solution(open_facilities)
    return open_facilities

# Returns those facilities that have their capacity exceeded given a specific assignment
def facilities_capacity_exceeded(demands, capacities, assignment):
    c = capacities.copy() 
    for client, facility in assignment.items():
        c[facility] -= demands[client]
    # Facilities to close
    return [j for j in range(len(capacities)) if c[j] < 0]