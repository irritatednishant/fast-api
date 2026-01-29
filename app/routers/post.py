
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from schemas import Post, CreatePost, ResponsePost
from sqlalchemy.orm import Session
from database import get_db
import models, oauth2


router = APIRouter()

@router.post("/create_post",status_code=status.HTTP_201_CREATED, response_model=ResponsePost)
def create_post(post : CreatePost,db : Session = Depends(get_db),user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (content,title,published)  VALUES(%s,%s,%s) RETURNING *""",
    #                (post.content, post.title, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    #new_post = models.Post(title=post.title,content=post.content,published=post.published)
    new_post = models.Post(owner_id = user.id, **post.model_dump()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    
@router.get("/getPost")
def get_post(db: Session = Depends(get_db),user : int = Depends(oauth2.get_current_user)):
    print(user.id)
    print(user.email)
    posts = db.query(models.Post).all()
    return posts



@router.post("/get_post/{id}",  response_model=ResponsePost)
def get_post(id: int,db : Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found!")
    return post


@router.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int,db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FORM posts WHERE id = %s RETURNING * """,str(id))
    # deleted = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorisez to perform requested action!")
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found!")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/update/{id}")
def update_post(new_post : Post,id : int, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorisez to perform requested action!")
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found!")
    post_query.update(new_post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()


