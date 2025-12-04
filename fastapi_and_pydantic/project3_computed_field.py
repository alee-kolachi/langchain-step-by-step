from pydantic import BaseModel, Field, EmailStr, AnyUrl, field_validator, model_validator, computed_field
from typing import Annotated, Optional

class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    linkedin_url: AnyUrl
    contact_details: Optional[str] = None
    weight: float
    height: float

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2),2)
        return bmi


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.linkedin_url)
    print(patient.bmi)
    
    print("Inserted")

patient_info = {
    "name": "Alee",
    "age": 55,
    "email": "alee.kola@gm.pk",
    "linkedin_url": "https://a.com",
    "contact_details": "{'emergency':'number'}",
    "weight": 61,
    "height": 1.71
}

patient1 = Patient(**patient_info)
insert_patient_data(patient1)