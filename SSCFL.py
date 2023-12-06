from random_helper import uniform, sample, get_uniform_distribution
from data_helper import initialize_dict
from itertools import product

# Deprecated

class FacilityLocation:
    def __init__(self, number_of_clients, number_of_facilities):
        n = number_of_clients
        m = number_of_facilities
        N = list(range(n))
        M = list(range(m))    
        self.demands = [0 for i in N]
        self.capacities = [0 for j in M]
        self.facility_costs = [0 for j in M]
        self.route_costs = initialize_dict(list(product(N, M)), 0) # keys: (client, facility)
        self.preferences = initialize_dict(N, [-1 for j in M]) # keys: client; value: list / list-index: preference-ranking; list-value: facility, 0 to m-1, 0 = top preference
        self.rankings = initialize_dict(N, [-1 for j in M]) # keys: client; value: list / list-index: facility; list-value: preference-ranking
        
        self.solution_facilities_to_open = []
        self.solution_assignments = initialize_dict(N, -1) # keys: client
        self.server_list = initialize_dict(M, []) # keys: facility
        self.issues = [] # Contains information about infeasible solutions

    #########################################################################################
    #/////////Set demands, capacities, facility cost, route costs, and preferences//////////#
    #########################################################################################
    def set_demand_at(self, client_i, demand):
        assert demand >= 0
        self.demands[client_i] = demand

    def set_capacity_at(self, facility_j, capacity):
        assert capacity >= 0
        self.capacities[facility_j] = capacity

    def set_facility_cost_at(self, facility_j, cost):
        assert cost >= 0
        self.facility_costs[facility_j] = cost

    def set_route_cost_at(self, client_i, facility_j, cost):
        assert cost >= 0
        self.route_costs[(client_i, facility_j)] = cost
    
    def set_preferences_of(self, client_i, preferences):
        m = len(self.capacities)
        assert len(preferences) == m
        for j in range(m):
            assert j in preferences
            # Set rankings on the way
            self.rankings[client_i][preferences[j]] = j 
        self.preferences[client_i] = preferences.copy()

    ################################################################################################################
    # Set demands, capacities, facility cost, route costs, and preferences according to a probability distribution #
    ################################################################################################################
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

    def set_preferences_randomly(self, probability_distribution):
        m = len(self.capacities)
        assert len(probability_distribution) == m
        for i in range(len(self.demands)):
            # Create a random preference list
            preference_list = []
            copy_of_prob_dist = probability_distribution.copy()
            M = list(range(m))
            for _ in range(m):
                # Determine next facility
                facility = sample(M, copy_of_prob_dist, eliminate_almost_never_probabilities = True)
                preference_list.append(facility)
                # Remove option to pick that facility again
                copy_of_prob_dist[facility] = 0
            # Assign it
            self.set_preferences_of(i, preference_list)

    #########################################################################################
    #///////////////////////////// Preference factory // ///////////////////////////////////#
    #########################################################################################
    def set_preferences_according_to(self, category):
        match category:
            case 0:
                self.set_preferences_as_distance()
            case 1:
                m = self.number_of_facilities()
                self.set_preferences_randomly(get_uniform_distribution(m))
            case _:
                assert False

    def set_preferences_as_distance(self, lexicographic = True):
        for client in range(self.number_of_clients()):
            facility_distance_pairs = [(j, self.route_costs[(client, j)]) for j in range(self.number_of_facilities())]
            facility_distance_pairs.sort(key=lambda pair: pair[1])
            self.set_preferences_of(client, [facility for (facility, _) in facility_distance_pairs])
    #########################################################################################
    #/////////////////////////////////// Get information ///////////////////////////////////#
    #########################################################################################
    def number_of_clients(self):
        return len(self.demands)
    
    def number_of_facilities(self):
        return len(self.capacities)

    def get_demands(self):
        return self.demands.copy()
    
    def get_capacities(self):
        return self.capacities.copy()
    
    def get_facility_costs(self):
        return self.facility_costs.copy()
    
    def get_route_costs(self):
        return self.route_costs.copy()
    
    def get_preferences(self, client):
        return self.preferences[client].copy()
    
    def get_rankings(self, client):
        return self.rankings[client].copy()
    
    def get_demands_by_server_list(self, facility):
        cumulative_demand = 0
        for client in self.server_list[facility]:
            cumulative_demand += self.demands[client]
        return cumulative_demand
    
    #########################################################################################
    #////////////////////// Methods revolving around a solution ////////////////////////////#
    #########################################################################################
    # Set solution
    def set_solution(self, facilities_to_open, assignments):
        self.issues = ["Solution has not yet been checked"]
        self.solution_facilities_to_open = facilities_to_open.copy()
        self.solution_assignments = assignments.copy()
        self.server_list = initialize_dict(list(range(self.number_of_facilities())), []) # Reset server list
        for client, facility in self.solution_assignments.items():
            self.server_list[facility].append(client)
    
    # Feasibility check
    def feasible(self): 
        self.issues = []
        for client in range(self.number_of_clients()):
            # Every client is served
            if client not in self.solution_assignments.keys():
                self.issues.append(str("Client " + str(client) + " is not served"))
            else:
                # No client is sent to a closed facility
                facility = self.solution_assignments[client]
                if facility not in self.solution_facilities_to_open:
                    self.issues.append(str("Client " + str(client) + " is served at closed facility " + str(facility)))
                # Preferences
                for facility in self.preferences[client]:
                    if facility in self.solution_facilities_to_open:
                        if facility != self.solution_assignments[client]:
                            self.issues.append(str("Client " + str(client) + " is assigned to " + str(self.solution_assignments[client]) + " but " + str(facility) + " is more preferred"))
                        break
        # Capacities
        for facility in self.solution_facilities_to_open:
            if self.get_demands_by_server_list(facility) > self.capacities[facility]:
                self.issues.append(str("Capacity is violated for facility " + str(facility)))
        return not bool(self.issues)
    
    # Objective value
    def solution_value(self):
        res = 0
        for facility in self.solution_facilities_to_open:
            res += self.facility_costs[facility]
        for client, facility in self.solution_assignments.items():
            res += self.route_costs[(client, facility)]
        return res
    
    #########################################################################################
    #/////////////////////////// Print instance information ////////////////////////////////#
    #########################################################################################
    def status(self, print_issues = False):
        print("##### ##### ##### ##### ##### ##### ##### ##### ##### #####")
        for facility in self.solution_facilities_to_open:
            print("Facility", facility, "serves clients", self.server_list[facility] ,"at", self.get_demands_by_server_list(facility), "/", self.capacities[facility])
        print("The computed solution is:", self.solution_facilities_to_open)
        if self.feasible():
            print("The solution is feasible")
        else:
            print("The solution is infeasible")
            if print_issues:
                for issue in self.issues:
                    print(issue)
        print("The total cost is", self.solution_value())
        print("##### ##### ##### ##### ##### ##### ##### ##### ##### #####")  

    