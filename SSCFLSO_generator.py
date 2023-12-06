from data_helper import initialize_dict
from math import sqrt
from random import uniform, triangular
from itertools import product

class FL_Generator:
    def __init__(self, n, m):
        self.I = list(range(n))
        self.J = list(range(m))

        self.travel_costs = initialize_dict(list(product(self.I, self.J)), 0)
        self.opening_costs = [0 for j in self.J]
        self.demands = [0 for i in self.I]
        self.capacities = [0 for j in self.J]
        self.preferences = initialize_dict(self.I, self.J)

    def set_opening_costs(self, opening_cost_function):
        self.opening_costs = [opening_cost_function() for j in self.J]

    def set_travel_costs(self, travel_cost_function):
        for (client, facility) in self.travel_costs.keys():
            self.travel_costs[(client, facility)] = travel_cost_function(client, facility)

    def set_demands(self, demand_function):
        self.demands = [demand_function() for i in self.I]

    def set_capacities(self, capacity_function):
        self.capacities = [capacity_function() for j in self.J]

    def set_preference(self, category):
        match category:
            case 0:
                # Preferences = Travel Distance
                for i in self.I:
                    by_travel_costs = [(j, self.travel_costs[(i, j)]) for j in self.J]
                    by_travel_costs.sort(key = lambda x: x[1])
                    self.preferences[i] = [j for (j, _) in by_travel_costs]
            case 1:
                # Preferences = Travel Distance from a triangular distribution
                for i in self.I:
                    min_i = min([self.travel_costs[(i,j)] for j in self.J])
                    max_i = max([self.travel_costs[(i,j)] for j in self.J])
                    fake_costs = [(j, triangular(min_i, max_i, self.travel_costs[(i, j)])) for j in self.J]
                    fake_costs.sort(key = lambda x: x[1])
                    self.preferences[i] = [j for (j, _) in fake_costs]
            case _:
                assert False

    def get_instance(self):
        return (self.I.copy(), self.J.copy(), self.travel_costs.copy(), self.opening_costs.copy(), self.demands.copy(), self.capacities.copy(), self.preferences.copy())

    def i300(self):
        # Place points uniformly and randomly in a unit square
        # Travel cost is 10 times the euclidean distance
        # Demands are drawn from U[5, 35]
        # Capacities are drawn from U[10, 160] then scaled by r = sum of all capacities/full demand
        # Opening costs are drawn from U[0, 90] + U[100, 110] * sqrt(capacity)
        u = lambda : uniform(0, 1)
        clients = [(u(), u()) for _ in self.I]
        facilities = [(u(), u()) for _ in self.J]
        for (i,j) in self.travel_costs.keys():
            c_x = clients[i][0]
            c_y = clients[i][1]
            f_x = facilities[j][0]
            f_y = facilities[j][1]
            self.travel_costs[(i, j)] = 10 * sqrt(((c_x - f_x) ** 2) * ((c_y - f_y) ** 2))
        d = lambda : uniform(5, 35)
        self.set_demands(d)

        preliminary_capacities = [uniform(10, 160) for _ in self.J]
        C = sum(preliminary_capacities)
        D = sum(self.demands)
        ratio = C/D
        self.capacities = [ratio*c for c in preliminary_capacities]
        self.opening_costs = [uniform(0, 90) + uniform(100, 110) * sqrt(capacity) for capacity in self.capacities]
