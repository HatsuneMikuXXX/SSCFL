from random_helper import flip


class FacilityLocation:
    def __init__(self):
        self.sex = 0
    
    def get_instance(n, m, d_min, d_max, u_min, u_max, c_min, c_max):
        C = list(range(1, n + 1))
        F = list(range(1, m + 1))
        return [C, F]

class Client:
    def __init__(self, id, demand):
        self.id = id
        self.demand = demand
        self.facility = 0

    def id(self):
        return self.id
    
    def demand(self):
        return self.demand
    
    def facility(self, id):
        self.facility = id

    def status(self):
        print("Client", self.id, ":")
        if self.facility == 0:
            print("Is not served")
        else:
            print("Is served by Facility", self.facility)

class Facility:
    def __init__(self, id, capacity):
        self.id = id
        self.current_capacity = 0
        self.capacity = capacity
        self.capacity_reached = False
        self.capacity_exceeded = False
        self.clients = []

    def id(self):
        return self.id

    def capacity(self):
        return self.capacity
    
    def add_client(self, client):
        if client not in self.clients:
            self.clients.add(client)
            client.facility(self.id)
        self.current_capacity += client.demand()
        self.update()

    def remove_client(self, client):
        if client in self.clients:
            self.clients.remove(client)
            client.facility(0)
        self.current_capacity -= client.demand()
        self.update()

    def update(self):
        self.capacity_reached = self.current_capacity >= self.capacity
        self.capacity_exceeded = self.current_capacity > self.capacity

    def status(self):
        print("Facility", self.id, ":")
        if not self.capacity_reached:
            print("Can still serve more clients")
        else:
            if not self.capacity_exceeded:
                print("Limit reached")
            else:
                print("Limit exceeded")
        print("Serving: ", end = "")
        for client in self.clients:
            print(client.id(), end = ", ")
            


for i in range(100):
    print(flip(), end = "")