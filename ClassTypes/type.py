from typing import List, Optional,Dict
from pydantic import BaseModel, EmailStr, HttpUrl, Field, field_validator
from datetime import date


class HTMLData(BaseModel):
    html: str

