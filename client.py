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