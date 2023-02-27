from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class AutheticationModel(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "misha92",
                "password": "123456",
            }}

class StudentModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)
    course: str = Field(...)
    age: int = Field(..., ge=0)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "misha@gmail.com",
                "username": "misha92",
                "password": "123456",
                "course": "ITMO WAD",
                "age": "18",
            }
        }


class UpdateStudentModel(BaseModel):
    name: Optional[str]
    username: Optional[str]
    password: Optional[str]
    email: Optional[EmailStr]
    course: Optional[str]
    age: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "misha@gmail.com",
                "username": "misha92",
                "password": "123456",
                "course": "ITMO WAD",
                "age": "18",
            }
        }
