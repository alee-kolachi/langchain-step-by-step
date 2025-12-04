from pydantic import BaseModel

class Address(BaseModel):
    city: str
    country: str
    postal_code: int

class Student(BaseModel):
    name: str
    number: str
    address: Address
    age: int = 20

address_dict = {"city": "Larkana", "country": "Pakistan", "postal_code": 77150}
address1 = Address(**address_dict)

student_dict = {"name": "Ali", "number": "101034", "address": address1}
student1 = Student(**student_dict)

print(student1)

print(student1.model_dump())
print(type(student1.model_dump()))

print(student1.model_dump_json())
print(type(student1.model_dump_json()))

print(student1.model_dump(exclude=["name"]))

print(student1.model_dump(exclude_unset=True))