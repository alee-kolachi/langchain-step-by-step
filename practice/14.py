
x = {
    "name": "Hussain",
    "age": 20,
    "marital_status": False,
    "children": [],
    "cars": [
        {"model": 2020, "brand": "bmw"},
        {"model": 2000, "brand": "range rover"}
    ],
    "college": "Bahria"
}

print(type(x))

print(x.items())


y = "Degree College"

x["college"] = y

print(x)

x.pop("marital_status")

print(x)