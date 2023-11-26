from random_helper import uniform, sample
from itertools import product

class FacilityLocation:
    def __init__(self, number_of_clients, number_of_facilities):    
        self.demands = [0 for i in range(number_of_clients)]
        self.capacities = [0 for j in range(number_of_facilities)]
        self.facility_cost = [0 for j in range(number_of_facilities)]
        self.route_costs = dict({}) # keys: (client, facility)
        self.preferences = dict({}) # keys: client; value: list / list-index: preference-ranking; list-value: facility, 0 to m-1, 0 = top preference
        
        self.solution_facilities_to_open = []
        self.solution_assignments = dict({}) # keys: client

    # Set demands, capacities, facility cost, route costs, and preferences
    def set_demand_at(self, client_i, demand):
        assert demand >= 0
        self.demands[client_i] = demand

    def set_capacity_at(self, facility_j, capacity):
        assert capacity >= 0
        self.capacities[facility_j] = capacity

    def set_facility_cost_at(self, facility_j, cost):
        assert cost >= 0
        self.facility_cost[facility_j] = cost

    def set_route_cost_at(self, client_i, facility_j, cost):
        assert cost >= 0
        self.route_costs[(client_i, facility_j)] = cost
    
    def set_preferences_of(self, client_i, preferences):
        n = len(self.capacities)
        assert len(preferences) == n
        for i in range(n):
            assert i in preferences
        self.preferences[client_i] = preferences

    # Set demands, capacities, facility cost, route costs, and preferences according to a probability distribution
    def set_demands_randomly(self, demands, probability_distribution, discrete = True):
        if discrete:
            for i in range(len(self.demands)):
                self.set_demand_at(i, sample(demands, probability_distribution))
        else:
            lb = min(demands)
            ub = max(demands)
            for i in range(len(self.demands)):
                self.set_demand_at(i, uniform(lb, ub))

    def set_capacities_randomly(self, capacities, probability_distribution, discrete = True):
        if discrete:
            for j in range(len(self.capacities)):
                self.set_capacity_at(j, sample(capacities, probability_distribution))
        else:
            lb = min(capacities)
            ub = max(capacities)
            for j in range(len(self.capacities)):
                self.set_capacity_at(j, uniform(lb, ub))

    def set_facility_costs_randomly(self, costs, probability_distribution, discrete = True):
        if discrete:
            for j in range(len(self.capacities)):
                self.set_facility_cost_at(j, sample(costs, probability_distribution))
        else:
            lb = min(costs)
            ub = max(costs)
            for j in range(len(self.capacities)):
                self.set_facility_cost_at(j, uniform(lb, ub))

    def set_route_costs_randomly(self, costs, probability_distribution, discrete = True):
        N = list(range(len(self.demands)))
        M = list(range(len(self.capacities)))
        if discrete:
            for i, j in product(N, M):
                self.set_route_cost_at(i, j, sample(costs, probability_distribution))
        else:
            lb = min(costs)
            ub = max(costs)
            for i, j in product(N, M):
                self.set_route_cost_at(i, j, uniform(lb, ub))

    def set_prefereces_randomly(self, probability_distribution):
        m = len(self.capacities)
        assert len(probability_distribution) == m
        for i in range(len(self.demands)):
            # Create a random preference list
            preference_list = []
            copy_of_prob_dist = probability_distribution.copy()
            M = list(range(m))
            for j in range(m):
                # Determine next facility
                facility = sample(M, copy_of_prob_dist, eliminate_almost_never_probabilities = True)
                preference_list.add(facility)
                # Remove option to pick that facility again
                copy_of_prob_dist[facility] = 0
            # Assign it
            self.preferences[i] = preference_list

    # Set solution
    def set_solution(self, facilities_to_open, assignments):
        self.solution_facilities_to_open = facilities_to_open.copy()
        self.solution_assignments = assignments.copy()
    
    # Feasibility check
    def feasible(self):
        issues = []
        # Single Source, Capacities, Facility is open, Preferences
        for client, facility_list in self.solution_assignments.items():
            if len(facility_list) != 1:
                issues.add(str("Single-Source is violated for client", client))
                continue
            [facility] = facility_list
            if self.demands[client] > self.capacities[facility]:
                issues.add(str("Capacity is violated for client", client))
            if facility not in self.solution_facilities_to_open:
                issues.add(str("Facility", facility, "is closed but still assigned")) 
            for facility in self.preferences[client]:
                if facility in self.solution_facilities_to_open:
                    if facility != self.solution_assignments[client]:
                        issues.add(str("Client", client, "is assigned to", self.solution_assignments[client], "but", facility, "is more preferred"))
                    break
        return (bool(issues), issues)
    
    # Objective value
    def solution_value(self):
        res = 0
        for facility in self.solution_facilities_to_open:
            res += self.facility_cost[facility]
        for _, cost in self.solution_assignments.items():
            res += cost
        return res


    