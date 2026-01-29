from fastapi import FastAPI, Response, status, HTTPException, Depends
from random import randrange
# import psycopg2
from psycopg2.extras import RealDictCursor
import models
from database import get_db, engine
from sqlalchemy.orm import Session
from schemas import Student, Post, CreatePost, ResponsePost
from routers import post, user, auth
models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/sqlalchemy")
def test_post(db : Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/")
def root():
    return {"message" : "hello world"}

students =[{
    "id":103,
    "name":"nishant",
    "course":"bca",
        },
   {
    "id":104,
    "name":"anshul",
    "course":"bca",
        }
]

@app.get("/data")
def data():
    return {"student_info" : students}

def find_st(id):
    for p in students:
        if p['id'] == id:
         return p 

@app.post("/ent_st",status_code=status.HTTP_201_CREATED)
def create_student(student : Student):
    student_ = student.model_dump()
    student_['id'] = randrange(100,200)
    students.append(student_)
    return {"student_info" : students}

@app.get("/get_st/{id}")
def get_student(id: int,resp : Response):
    student = find_st(id)
    if not student:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found!") 
    #  resp.status_code = status.HTTP_400_BAD_REQUEST
    #  return {"message": "Student not found"}
    return {"student" : student}



#connecting to the database

# try:
#     conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Database connected successfully!")
# except Exception as error:
#     print("Connection to database failed !")
#     print("Error:" , error)



# @app.get("/posts")
# def get_post():
#     cursor.execute("""Select * from posts""")
#     posts = cursor.fetchall()
#     return {'data' : posts}




@app.get("/example")
def dummy():
    return {"data" : "hello sanchay!"}