class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def celebrate_birthday(self):
        #self.age = self.age + 1
        self.age += 1

        return f"HBD {self.name}"
    
p1 = Person("Basit", 10)
print(f"Before Birthday Age: {p1.age}")
print(p1.celebrate_birthday())
print(f"After Birthday Age: {p1.age}")