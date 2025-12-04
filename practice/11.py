class Person:
    """Person class"""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def celebrate_birthday(self):
        """The function will update the age and show the message"""
        #self.age = self.age + 1
        self.age += 1

        return f"HBD {self.name}"
    
p1 = Person("Basit", 10)
print(f"Before Birthday Age: {p1.age}")
print(p1.celebrate_birthday())
print(f"After Birthday Age: {p1.age}")


p2 = Person()