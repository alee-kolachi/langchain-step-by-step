from pydantic import BaseModel, Field, EmailStr, AnyUrl, field_validator, model_validator
from typing import Annotated, Optional

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=20, title="Name of the patient", description="Give the name please", examples=["Ali"])]
    age: int = Field(lt=200, gt=5)
    email: EmailStr
    linkedin_url: AnyUrl
    contact_details: Optional[str] = None

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_domains = ["gm.pk", ".org"]

        domain_name = value.split("@")[-1]
        if domain_name not in valid_domains:
            raise ValueError("Not a valid email")
        return value

    @field_validator("name")
    @classmethod
    def transform_name(cls, name):
        return name.upper()
    
    @model_validator(mode="after")
    def validate_emergency_contact(cls, model):
        if model.age > 50 and "emergency" not in model.contact_details:
            raise ValueError("Patient older than 50 must have emergency contact")
        return model



def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.linkedin_url)
    print("Inserted")

patient_info = {
    "name": "Alee",
    "age": 55,
    "email": "alee.kola@gm.pk",
    "linkedin_url": "https://a.com",
    "contact_details": "{'emergency':'number'}"
}

patient1 = Patient(**patient_info)
insert_patient_data(patient1)