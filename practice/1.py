class Student:

    def __init__(self, name, school, age=20):
        self.name = name
        self.age = age
        self.school = school


student1 = Student("ali", "degree college")

print(student1.age)
