# Returns an initial solution using the stingy heuristic then optimizing it further by closing non-serving open facilities.
def initial_solution(FacilityLocation):
    open_facilities = list(range(FacilityLocation.number_of_facilities())) # Open every facility
    edge_set = unique_edge_set(FacilityLocation, open_facilities)
    FacilityLocation.set_solution(open_facilities, edge_set)
    while bool(open_facilities) and not FacilityLocation.feasible():
        facilities_to_close = facilities_capacity_exceeded(FacilityLocation, edge_set)
        open_facilities = list(set(open_facilities) - set(facilities_to_close))
        edge_set = unique_edge_set(FacilityLocation, open_facilities)
        FacilityLocation.set_solution(open_facilities, edge_set)
    # Optimize by removing facilities that are open but never serve
    tmp = open_facilities.copy() # I do not know why exactly, but in general DO NOT iterate over stuff you are changing
    for facility in tmp:
        if FacilityLocation.get_demands_by_server_list(facility) == 0:
            open_facilities.remove(facility)
    FacilityLocation.set_solution(open_facilities, edge_set)
    return open_facilities

# Computes the unique assignment given the preferences and open facilities
def unique_edge_set(FacilityLocation, open_facilities):
    edge_set = dict({})
    if not bool(open_facilities):
        return edge_set
    for client in range(FacilityLocation.number_of_clients()):
        ranking_of_client = FacilityLocation.get_rankings(client)
        best_ranked_facility = open_facilities[0]
        for facility in open_facilities:
            if ranking_of_client[facility] < ranking_of_client[best_ranked_facility]:
                best_ranked_facility = facility
        edge_set[client] = best_ranked_facility
    return edge_set

# Returns those facilities that have their capacity exceeded given a specific assignment
def facilities_capacity_exceeded(FacilityLocation, assignment):
    demands = FacilityLocation.get_demands()
    capacities = FacilityLocation.get_capacities()
    for client, facility in assignment.items():
        capacities[facility] -= demands[client]
    # Facilities to close
    return [j for j in range(FacilityLocation.number_of_facilities()) if capacities[j] < 0]

        
