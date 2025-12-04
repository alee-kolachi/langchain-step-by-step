from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data


@app.get("/")
def hello():
    return "Hello world"

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{id}")
def view_patient(id):
    data = load_data()
    if id in data:
        return data[id]
    else:
        return {"error": "Patient not found"}