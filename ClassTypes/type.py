from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl, Field, field_validator
from datetime import date


class PersonalDetails(BaseModel):
    name: str
    email: EmailStr
    contact_no: Optional[str]
    country: Optional[str] 
    city: Optional[str] 


class RoleDetails(BaseModel):
    role: str
    linkedIn: HttpUrl
    summary: Optional[str] = None

    @field_validator("linkedIn")
    @classmethod
    def validate_linkedin_url(cls, value):
        if "linkedin.com/in/" not in value:
            raise ValueError("Invalid LinkedIn URL")
        return value


class EducationItem(BaseModel):
    Institute: str
    degree: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    location: str
    description: Optional[str] = None

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, end_date, values):
        start_date = values.get("start_date")
        if start_date and end_date and end_date < start_date:
            raise ValueError("End date cannot be before start date")
        return end_date


class WorkExperienceItem(BaseModel):
    company_name: str
    start_date: Optional[date] 
    end_date: Optional[date]
    role: str
    description: Optional[str] 
    location: str

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, end_date, values):
        start_date = values.get("start_date")
        if start_date and end_date and end_date < start_date:
            raise ValueError("End date cannot be before start date")
        return end_date


class Skills(BaseModel):
    fieldName: Optional[str] 
    data: str


class CustomFieldItem(BaseModel):
    header: str
    subHeader: Optional[str] 
    description: Optional[str] 


class CustomField(BaseModel):
    fieldName: str
    fields: List[CustomFieldItem]


class ResumeType(BaseModel):
    user_id: str
    resumeName: str
    personalDetails: PersonalDetails
    roleDetails: RoleDetails
    Education: List[EducationItem]
    WorkExperience: List[WorkExperienceItem]
    Skills: Skills
    CustomField: Optional[List[CustomField]] 

class HTMLData(BaseModel):
    html: str

