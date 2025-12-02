from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel ,Field, computed_field
from typing import Annotated, Literal
app = FastAPI()

class Student(BaseModel):
    id:Annotated[int, Field(...,description='ID of the student',)]
    name:Annotated[str,Field(...,description='Name of the student')]
    course:Annotated[str,Field(...,description='Course in which student is enrolled')]
    enrollment_no:Annotated[int,Field(...,gt=0,description='Enrollment no of the student')]
    address:Annotated[str,Field(...,description='Address of the student.')]
    gender:Annotated[Literal['Male','Female'],Field(...,description='Gender of the student')]
    cgpa:Annotated[float,Field(...,gt=0,le=10,description='CGPA of the student')]

    pass

def load_data():
    with open('student.json','r') as f:
        data = json.load(f) 
    return data


def save_obj(data):
    with open('student.json','w') as f:
        json.dump(data,f)


@app.get("/")
def hello():
    return {"message":"hello world"}

@app.get("/view")
def view():
    data = load_data()
    print(data)
    return data

@app.get("/student/{student_id}")
def view_student(student_id:str =Path(...,description="ID of student in db",examples='[1,2,3]')):
    data = load_data()
    student = next((s for s in data if s['id'] == int(student_id) ),None)
    if student:
        return student
    raise HTTPException(status_code=404, detail="Student not found!")


@app.get("/sort")
def sort_student(sort_by: str = Query(...,description='Sort student pn the basis of their name, enrolment and cgpa'),
                  order: str = Query('asc',description='Sort in asc or desc')):
    valid_fields = ['name','enrollment_no','cgpa']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order select between asc and desc')
    
    data = load_data()
    sort_order = True if order=='desc' else False

    sorted_data = sorted(data, key = lambda x: x[sort_by],reverse=sort_order)

    return sorted_data
    
@app.post('/create')
def create(student:Student):

    data = load_data()

    if any(int(student.id) == obj['id'] for obj in data):
        raise HTTPException(status_code=400,detail='Student already exists!')
    
    data.append(student.model_dump())

    save_obj(data)

    return JSONResponse(status_code=201,content={'message':'Student details added sucessfully!'})


if "__name__" == "__main__":
    data = load_data()
    print(data)
