from data_helper import initialize_dict

class FL_Validator:
    def __init__(self, number_of_facilities, number_of_clients, demands, capacities, opening_costs, travel_costs, preferences):
        self.J = list(range(number_of_facilities))
        self.I = list(range(number_of_clients))
        self.c = travel_costs
        self.f = opening_costs
        self.d = demands
        self.u = capacities
        self.preferences = preferences

        self.rankings = initialize_dict(self.I, [-1 for j in self.J])
        for i in self.I:
            rank = 0
            for j in self.preferences[i]:
                self.rankings[i][j] = rank
                rank += 1
        
        self.solution = []
        self.assignment = initialize_dict(self.I, -1)
        self.value = -1
        self.empty_solution = False
    
    def set_solution(self, open_facilities):
        m = len(self.J)
        k = len(open_facilities)
        self.solution = open_facilities.copy()
        if k == 0:
            self.empty_solution = True
            self.value = -1
            return
        else:
            self.empty_solution = False
        if (k ** 2) - 2*k - 1 >= m:
            # Expected number of checks using preferences is smaller than the number of checks using rankings
            # under the assumption that the open facilities are chosen uniformly at random
            for i in self.I:
                for j in self.preferences[i]:
                    if j in open_facilities:
                        self.assignment[i] = j
                        break
        else:
            for i in self.I:
                most_preferred = open_facilities[0]
                for j in open_facilities:
                    if self.rankings[i][j] < self.rankings[i][most_preferred]:
                        most_preferred = j
                self.assignment[i] = most_preferred
        self.update_value()

    def get_assignment(self):
        return self.assignment.copy() 
    
    def get_value(self):
        return self.value

    def feasible(self):
        if self.empty_solution:
            return False
        capacities = [self.u[j] for j in self.J]
        for i in self.I:
            capacities[self.assignment[i]] -= self.d[i]
            if capacities[self.assignment[i]] < 0:
                return False
        return True

    def update_value(self):
        self.value = 0
        for j in self.solution:
            self.value += self.f[j]
        for i in self.I:
            j = self.assignment[i]
            self.value += self.c[(j, i)]

