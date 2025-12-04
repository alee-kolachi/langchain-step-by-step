"""The __str__() Method
The __str__() method is a special method that controls what is returned when the object is printed:"""

class Village:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"HELLO, I AM AN OBJECT MY VILLAGE NAME IS {self.name}"

v1 = Village("Sehar Station")
print(v1.name)


print(v1)
        