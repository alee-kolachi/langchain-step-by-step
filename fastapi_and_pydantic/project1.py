from pydantic import BaseModel, Field, EmailStr, AnyUrl, field_validator
from typing import Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=20, title="Name of the patient", description="Give the name please", examples=["Ali"])]
    age: int = Field(lt=20, gt=5)
    email: EmailStr
    linkedin_url: AnyUrl

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


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.linkedin_url)
    print("Inserted")

patient_info = {
    "name": "Alee",
    "age": 10,
    "email": "alee.kola@gm.pk",
    "linkedin_url": "https://a.com"
}

patient1 = Patient(**patient_info)
insert_patient_data(patient1)