from data_helper import initialize_dict
from itertools import product
from math import sqrt
import os
from random import uniform, triangular


class FL_Generator:
    def __init__(self, m, n):
        self.J = list(range(m))
        self.I = list(range(n))
        
        self.travel_costs = initialize_dict(list(product(self.J, self.I)), 0)
        self.opening_costs = [0 for _ in self.J]
        self.demands = [0 for _ in self.I]
        self.capacities = [0 for _ in self.J]
        self.preferences = initialize_dict(self.I, self.J)

    def set_opening_costs(self, opening_cost_function):
        self.opening_costs = [opening_cost_function() for j in self.J]

    def set_travel_costs(self, travel_cost_function):
        for (facility, client) in self.travel_costs.keys():
            self.travel_costs[(facility, client)] = travel_cost_function(facility, client)

    def set_demands(self, demand_function):
        self.demands = [demand_function() for _ in self.I]

    def set_capacities(self, capacity_function):
        self.capacities = [capacity_function() for _ in self.J]

    def set_preferences(self, category):
        match category:
            case 0:
                # Preferences = Travel Distance
                for i in self.I:
                    by_travel_costs = [(j, self.travel_costs[(j, i)]) for j in self.J]
                    by_travel_costs.sort(key = lambda x: x[1])
                    self.preferences[i] = [j for (j, _) in by_travel_costs]
            case 1:
                # Preferences = Travel Distance from a triangular distribution
                for i in self.I:
                    min_i = min([self.travel_costs[(j,i)] for j in self.J])
                    max_i = max([self.travel_costs[(j,i)] for j in self.J])
                    fake_costs = [(j, triangular(min_i, max_i, self.travel_costs[(j, i)])) for j in self.J]
                    fake_costs.sort(key = lambda x: x[1])
                    self.preferences[i] = [j for (j, _) in fake_costs]
            case _:
                assert False

    def get_instance(self):
        return (len(self.J), len(self.I), self.demands.copy(), self.capacities.copy(), self.opening_costs.copy(), self.travel_costs.copy(), self.preferences.copy())
    
    # Format according to TBED1/Reame [Readme*] available at https://or-brescia.unibs.it/instances/instances_sscflp
    def save_instance(instance, filename, overwrite = False):
        (number_of_facilities, number_of_clients, demands, capacities, opening_costs, travel_costs, preferences) = instance
        line1 = str(number_of_facilities) + "\t" + str(number_of_clients)
        line2 = ""
        line3 = ""
        line4 = ""
        line5 = ""
        line6 = ""
        for d in demands:
            line2 += str(d) + "\t"
        for c in capacities:
            line3 += str(c) + "\t"
        for f in opening_costs:
            line4 += str(f) + "\t"
        for (facility, client), value in travel_costs.items():
            if facility > 0 and client == 0:
                line5 += "\n"
            line5 += str(value) + "\t"
        for facilities in preferences.values():
            for facility in facilities:
                line6 += str(facility) + "\t"
            line6 += "\n"
        line6 = line6[:-1]

        res = line1 + "\n\n" + line2 + "\n\n" + line3 + "\n\n" + line4 + "\n\n" + line5 + "\n\n" + line6
        if not os.path.exists(filename) or overwrite:
            file = open(filename, 'w')
            file.write(res)
            file.close()
        else:
            print("File already exists. To overwrite, set parameter 'overwrite' to True.")
            return False
        return True

    def load_instance(filename):
        # Parse data
        file = open(filename, 'r')
        content = file.read()
        file.close()
        
        # If there is a cooler and shorter method, please let me know
        content = content.replace("\n\n", ",")
        content = content.replace("\n", ",")
        content = content.replace("\t,", ",")
        content = content.replace("\t", ",")
        info = []
        value = ""
        for c in content:
            if c != ",":
                value += c
            else:
                info.append(float(value))
                value = ""
        
        # Extract data
        m = int(info[0])
        n = int(info[1])
        res = FL_Generator(m, n)
        current_index = 2
        # Demand
        for index in range(current_index, current_index + n):
            res.demands[index - current_index] = info[index]
        current_index += n

        # Capacity
        for index in range(current_index, current_index + m):
            res.capacities[index - current_index] = info[index]
        current_index += m

        # Facility Cost
        for index in range(current_index, current_index + m):
            res.opening_costs[index - current_index] = info[index]
        current_index += m

        # Travel Cost
        for j in range(m):
            for i in range(n):
                index = current_index + j*n + i
                res.travel_costs[(j, i)] = info[index]
        current_index += m*n

        # Preferences
        for i in range(n):
            lb = current_index + i*m
            ub = current_index + (i + 1) * m
            res.preferences[i] = [int(info[index]) for index in range(lb, ub)]
        return res.get_instance()
        

    def i300(self, filename = ""):
        # Place points uniformly and randomly in a unit square
        # Travel cost is 10 times the euclidean distance
        # Demands are drawn from U[5, 35]
        # Capacities are drawn from U[10, 160] then scaled by r = sum of all capacities/full demand
        # Opening costs are drawn from U[0, 90] + U[100, 110] * sqrt(capacity)
        u = lambda : uniform(0, 1)
        clients = [(u(), u()) for _ in self.I]
        facilities = [(u(), u()) for _ in self.J]
        for (j,i) in self.travel_costs.keys():
            c_x = clients[i][0]
            c_y = clients[i][1]
            f_x = facilities[j][0]
            f_y = facilities[j][1]
            self.travel_costs[(j, i)] = 10 * sqrt(((c_x - f_x) ** 2) * ((c_y - f_y) ** 2))
        d = lambda : uniform(5, 35)
        self.set_demands(d)

        preliminary_capacities = [uniform(10, 160) for _ in self.J]
        C = sum(preliminary_capacities)
        D = sum(self.demands)
        ratio = C/D
        self.capacities = [ratio*c for c in preliminary_capacities]
        self.opening_costs = [uniform(0, 90) + uniform(100, 110) * sqrt(capacity) for capacity in self.capacities]
        self.set_preferences(0)
        if filename != "":
            instance = self.get_instance()
            self.save_instance(instance, filename)
