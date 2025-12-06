from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel ,Field, computed_field
from typing import Annotated, Literal, Optional
app = FastAPI()

class Student(BaseModel):
    id:Annotated[int, Field(...,description='ID of the student',)]
    name:Annotated[str,Field(...,description='Name of the student')]
    course:Annotated[str,Field(...,description='Course in which student is enrolled')]
    enrollment_no:Annotated[str,Field(...,description='Enrollment no of the student')]
    address:Annotated[str,Field(...,description='Address of the student.')]
    gender:Annotated[Literal['Male','Female'],Field(...,description='Gender of the student')]
    cgpa:Annotated[float,Field(...,gt=0,le=10,description='CGPA of the student')]

    
class StudentUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    course:Annotated[Optional[str],Field(default=None)]
    enrollment_no:Annotated[Optional[str],Field(default=None)]
    address:Annotated[Optional[str],Field(default=None)]
    gender:Annotated[Optional[Literal['Male','Female']],Field(default=None)]
    cgpa:Annotated[Optional[float],Field(gt=0,le=10,default=None)]


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


@app.put('/edit/{student_id}')
def update_student(student_id:str,student_update:StudentUpdate):
    data = load_data()
    
    existing_student_info = next((obj for obj in data if obj['id'] == int(student_id)) , None)
    if not existing_student_info:
        raise HTTPException(status_code=404, detail='Student not found!')
    
    updated_student_info = student_update.model_dump(exclude_unset=True)

    for key, value in updated_student_info.items():
        existing_student_info[key] = value
    
    
    student_pydantic_obj = Student(**existing_student_info)
    updated_data = student_pydantic_obj.model_dump()
    
    
    for i, student in enumerate(data):
        if student["id"] == int(student_id):
            data[i] = updated_data
            break

    save_obj(data)
    return JSONResponse(status_code=200, content={'message': 'Student updated successfully!'})

  
@app.delete('/delete/{student_id}')
def delete(student_id: int):
    data = load_data()
    del_student = next((i for i,obj in enumerate(data) if obj['id'] == int(student_id)),None)
    if not del_student:
        raise HTTPException(status_code=402, detail="Student not found!")
    del data[del_student]
    save_obj(data)

    return JSONResponse(status_code=200, content={'message':'Student deleted successfully!'})




if "__name__" == "__main__":
    data = load_data()
    print(data)
