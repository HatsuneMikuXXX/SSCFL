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