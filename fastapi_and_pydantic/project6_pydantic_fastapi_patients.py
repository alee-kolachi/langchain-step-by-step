from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated
import json

class Address(BaseModel):
    Street: Annotated[str, Field(description="Enter the street", examples=["Street 20"])]
    city: Annotated[str, Field(..., description="Enter the city please", examples=["Larkana"])]
    country: Annotated[str, Field(..., description="Enter the country please", examples=["Pakistan"])]
    postal: Annotated[int, Field(..., description="Postal code of the address", examples=[77150])]

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Enter the ID", examples=["P001"])]
    name: Annotated[str, Field(..., description="Enter the name of the patient", examples=["Manan"])]
    age: Annotated[int, Field(..., gt=0, description="Enter the age of the patient", strict=True, examples=[23])]
    weight: Annotated[float, Field(..., gt=0, description="Enter the weight in kg", examples=[66.1], strict=True)]
    height: Annotated[float, Field(..., gt=0, description="Enter the height in metres", examples=[1.7], strict=True)]
    address: Address

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 10:
            return "low BMI"
        elif self.bmi > 10:
            return "OKAY BMI"
        
    
def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data
    
def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

app = FastAPI()

@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    #New patient add to the data
    data[patient.id] = patient.model_dump(exclude=["id"])

    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})



