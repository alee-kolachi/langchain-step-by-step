class Person:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        message = f"Welcome {self.name}"
        return message
    
    def morning_greet(self):
        message1 = self.greet()
        message2 = f"\nGood morning"
        message = message1 + message2
        return message
    
person1 = Person("ali")

print(person1.morning_greet())
