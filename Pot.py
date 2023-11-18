def Pot():
    def __init__(self):
        self.value = 0

    def add(self, amount):
        self.value = self.value + amount
    
    def getValue(self):
        return self.value
    
    def reset(self):
        self.value = 0