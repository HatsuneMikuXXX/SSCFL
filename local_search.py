def initial_solution(FacilityLocation):
    open_facilities = list(range(FacilityLocation.number_of_facilities())) # Open every facility
    edge_set = unique_edgeset(FacilityLocation, open_facilities)
    FacilityLocation.set_solution(open_facilities, edge_set)
    while not bool(open_facilities) and FacilityLocation.feasible():
        facilities_to_close = facilities_capacity_exceeded(FacilityLocation, edge_set)
        open_facilities = list(set(open_facilities) - set(facilities_to_close))
        edge_set = unique_edgeset(FacilityLocation, open_facilities)
        FacilityLocation.set_solution(open_facilities, edge_set)
    return open_facilities

def unique_edgeset(FacilityLocation, open_facilities):
    edge_set = dict({})
    if bool(open_facilities):
        return edge_set
    for client in range(FacilityLocation.number_of_clients()):
        ranking_of_client = FacilityLocation.rankings(client)
        best_ranked_facility = open_facilities[0]
        for facility in open_facilities:
            if ranking_of_client[facility] > ranking_of_client[best_ranked_facility]:
                best_ranked_facility = facility
        edge_set[client] = best_ranked_facility
    return edge_set

def facilities_capacity_exceeded(FacilityLocation, assignment):
    demands = FacilityLocation.demands()
    capacities = FacilityLocation.capacities()
    for client, facility in assignment.items():
        capacities[facility] -= demands[client]

    # Facilities to close
    return [j for j in range(FacilityLocation.number_of_facilities()) if capacities[j] < 0]

        