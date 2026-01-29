from pydantic import BaseModel, Field, EmailStr
from typing import Annotated , Optional
from datetime import datetime
#from email import 

class Student(BaseModel):
    id:Annotated[int,Field(description="id of the student")]
    name:Annotated[str,Field(...,description="name of the student")]
    course:Annotated[str,Field(...,description="course of the student")]


class BasePost(BaseModel):
    content:Annotated[str,Field(...,description="Content of the post")]
    title:Annotated[str,Field(...,description="Title of the post")]
    published:Annotated[bool,Field(description="If the post is published or not!",default=False)]

class CreatePost(BasePost):
    #id:Annotated[int,Field(description="Id of the post!")]
    content:Annotated[str,Field(...,description="Content of the post")]
    title:Annotated[str,Field(...,description="Title of the post")]
    published:Annotated[bool,Field(description="If the post is published or not!",default=False)]
    #created_at:Annotated[str,Field(description="Time when the post was created!")]

class ResponsePost(BasePost):
    id:Annotated[int,Field(description="Id of the post!")]
    content:Annotated[str,Field(...,description="Content of the post")]
    title:Annotated[str,Field(...,description="Title of the post")]
    published:Annotated[bool,Field(description="If the post is published or not!",default=False)]
    created_at:Annotated[datetime,Field(description="Time when the post was created!")]
    model_config = {
        "from_attributes": True
    }

    
class Post(BasePost):
    pass
    

class User(BaseModel):
    email : Annotated[EmailStr,Field(...,description="email of user")]
    password : Annotated[str,Field(...,description="password of user")]

class userResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    model_config = {
        "from_attributes": True
    }

class UserLoging(BaseModel):
    email : EmailStr
    password : str


class TokenData(BaseModel):
    id : Annotated[Optional[int],Field(default=None)]
    