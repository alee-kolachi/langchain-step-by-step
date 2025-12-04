class Square:
    def __init__(self, length, width):

        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width
    
s1 = Square(10, 10)
s1.name = "Square 1"
s2 = Square(30, 20)

print(s1.area())
print(s2.area())

print(s1.name)