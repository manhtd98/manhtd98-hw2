import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
import motor.motor_asyncio
import uvicorn 
import hashlib
from models import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL", "mongodb+srv://finseed2021:finseed2021@cluster0.lmz9v.mongodb.net/?retryWrites=true&w=majority"))
db = client.students


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/", response_description="Add new student", response_model=StudentModel)
async def create_student(student: StudentModel = Body(...)):
    student = jsonable_encoder(student)
    student['password'] = hashlib.sha256(student['password'].encode()).hexdigest()
    new_student = await db["students"].insert_one(student)
    created_student = await db["students"].find_one({"_id": new_student.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)

@app.post("/auth", response_description="Authetication student info", response_model=StudentModel)
async def auth_student(user: AutheticationModel = Body(...)):
    user = jsonable_encoder(user)
    user['password'] = hashlib.sha256(user['password'].encode()).hexdigest()
    auth_student = await db["students"].find_one(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=auth_student)



@app.get(
    "/", response_description="List all students", response_model=List[StudentModel]
)
async def list_students():
    students = await db["students"].find().to_list(1000)
    return students


@app.get(
    "/{id}", response_description="Get a single student", response_model=StudentModel
)
async def show_student(id: str):
    if (student := await db["students"].find_one({"_id": id})) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.put("/{id}", response_description="Update a student", response_model=StudentModel)
async def update_student(id: str, student: UpdateStudentModel = Body(...)):
    student = {k: v for k, v in student.dict().items() if v is not None}

    if len(student) >= 1:
        update_result = await db["students"].update_one({"_id": id}, {"$set": student})

        if update_result.modified_count == 1:
            if (
                updated_student := await db["students"].find_one({"_id": id})
            ) is not None:
                return updated_student

    if (existing_student := await db["students"].find_one({"_id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete("/{id}", response_description="Delete a student")
async def delete_student(id: str):
    delete_result = await db["students"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


if __name__ == "__main__":
    uvicorn.run("app:app",host='0.0.0.0', port=5001, reload=True)