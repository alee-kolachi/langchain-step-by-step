import json

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

y = ("apple", "banana")

print(json.dumps(x, indent=1, sort_keys=True))
print(json.dumps(y))
