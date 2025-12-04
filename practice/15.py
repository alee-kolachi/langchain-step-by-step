"""Loop Through a Dictionary
You can loop through a dictionary by using a for loop.

When looping through a dictionary, the return value are the keys of the dictionary, but there are methods to return the values as well."""


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


for variable in x:
    print(f"{variable} -> {x[variable]}")

for index, variable in enumerate(x, 1):
    print(f"{index}. {variable} -> {x[variable]}")


for x in x.values():
    print(x)
