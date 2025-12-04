class Person:
    lastname = "Kolachi"

    def __init__(self, name):
        self.name = name

person1 = Person("ali")

print(person1.name)
print(person1.lastname)


person2 = Person("husain")

print(person2.name)
print(person2.lastname)



Person.lastname = "XYZ"
print("="*60)
print(person1.lastname)
print(person2.lastname)