import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app import models, schemas, oauth2
from typing import List, Optional
from fastapi import Depends,  Response, status, HTTPException, APIRouter
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user : schemas.UserResponse = Depends(oauth2.get_current_user), search : Optional[str] = "", limit : int = 10, skip:int=0):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall() # Use fetchall while getting multiple posts
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_post(id:int, db: Session = Depends(get_db), current_user : schemas.UserResponse = Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} not found.")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action.")
    return post
       
# After post creation, status code 201 should sent back.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : schemas.UserResponse = Depends(oauth2.get_current_user)):
    # do not use """ INSERT INTO posts (title, content) VALUES ({post.title}, {post.content})""", if user types a title like INSERT into, it will raise an error
    #cursor.execute(""" INSERT INTO posts (title, content) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content))
    #new_post = cursor.fetchone()
    #conn.commit()

    new_post = models.Post(user_id = current_user.id, **dict(post)) # instead of writing one by one, use **post.dict()
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# status code 204 should be sent back if the deletion is succesfull.
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db : Session = Depends(get_db), current_user : schemas.UserResponse = Depends(oauth2.get_current_user)):
    #cursor.execute(""" DELETE * FROM posts WHERE id = %s RETURNİNG * """, (str(id)))
    #deleted_post = cursor.fetcone()
    post_query  = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found.")
    if post_query.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action.")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

    # Using the line below won't work, after sending status code 204 you cannot simply return another data.
    # return {"message":f"Post {id} deleted."}

    # Instead, use this:
    
    
@router.put("/{id}")
def update_post(id:int, post: schemas.PostCreate, db : Session = Depends(get_db), current_user : schemas.UserResponse = Depends(oauth2.get_current_user)):
    #cursor.execute(""" UPDATE posts SET title = %s, content = %S, WHERE id = %s RETURNİNG * """, (post.title, post.content, str(id)))
    #updated_post = cursor.fetcone()
    post_query  = db.query(models.Post).filter(models.Post.id == id)


    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} not found.")
    if post_query.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action.")
    
    post_query.update(dict(post), synchronize_session=False)
    db.commit()
    
    return f"Post {id} is updated."