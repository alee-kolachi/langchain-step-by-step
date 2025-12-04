import json

x = """{
    "name": "ali",
    "caste": "Kolachi"
}"""


print(type(x))
y = json.loads(x)

print(type(y))
#############################

x = {
    "name": "ali",
    "caste": "Kolachi"
}


print(type(x))
y = json.dumps(x)

print(type(y))