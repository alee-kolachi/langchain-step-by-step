class Car:
    car_company = "ALI'S CAR COMPANY"
    
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model


toyota2020 = Car("Toyota", 2020)


print(toyota2020.brand)
print(toyota2020.model)
print()


del toyota2020.model

print(Car.car_company)
