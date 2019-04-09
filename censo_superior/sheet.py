class Sheet:
    def __init__(self, name, data):
        self.name = name
        self.data = data
    
    def __str__(self):
        return self.name + ": " + str(self.data)
    
    def __repr__(self):
        return_string = self.name

        if self.data and len(self.data):
            return_string += ": " + str(list(self.data[0].keys()))

        return return_string
