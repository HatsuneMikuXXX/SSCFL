from client import Client
from facility import Facility
from random_helper import uniform
from itertools import product

class FacilityLocation:
    def __init__(self):
        self.C = list([])
        self.F = list([])
        self.routes = dict({})
    
    def get_instance(self, n, m, d_min, d_max, u_min, u_max, c_min, c_max):
        assert d_max - d_min >= 0
        assert u_max - u_min >= 0
        assert c_max - c_min >= 0
        self.C = [Client(i, uniform(d_min, d_max)) for i in range(n)]
        self.F = [Facility(j, uniform(u_min, u_max)) for j in range(m)]
        for client, facility in product(self.C, self.F):
            self.routes[(client.id(), facility.id())] = uniform(c_min, c_max)

    