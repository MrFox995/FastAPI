from typing import List, Optional

from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix = "/sqlalchemy/posts", tags = ["Posts"])

@router.get("/", response_model = List[schemas.PostResponseV2])
def get_posts_ORM(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # OLD: posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_ID).label("votes_number")).join(models.Vote, models.Vote.post_ID == models.Post.ID, isouter = True).group_by(models.Post.ID).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = [schemas.PostResponseV2(post = post, votes_number = votes) for post, votes in results]

    return posts

@router.get("/myPosts", response_model = List[schemas.PostResponse])
def get_posts_ORM(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_ID == user_id.ID).all()

    return posts

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_posts_ORM(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.model_dump(), owner_ID = user_id.ID) # OLD: models.Post(title = post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model = schemas.PostResponseV2)
def get_post_ORM(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # OLD: post = db.query(models.Post).filter(models.Post.ID == id).first()
    result = db.query(models.Post, func.count(models.Vote.post_ID).label("votes_number")).join(models.Vote, models.Vote.post_ID == models.Post.ID, isouter = True).group_by(models.Post.ID).filter(models.Post.ID == id).first()

    if not result:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} was not found')
    print(result)
    post = schemas.PostResponseV2(post = result[0], votes_number = result[1])
    return post

@router.get("/myPost/{id}", response_model = schemas.PostResponse)
def get_post_ORM(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.ID == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} was not found')
    if post.owner_ID != user_id.ID:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f'Not authorized to perform the requested action')
    
    return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post_ORM(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.ID == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} doesn\'t exist')
    if post.owner_ID != user_id.ID:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f'Not authorized to perform the requested action')
    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model = schemas.PostResponse)
def update_posts_ORM(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.ID == id)
    fetched_post = post_query.first()

    if fetched_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} doesn\'t exist')
    if fetched_post.owner_ID != user_id.ID:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f'Not authorized to perform the requested action')
    
    post_query.update(post.model_dump(), synchronize_session = False)
    db.commit()

    db.refresh(fetched_post)
    return fetched_post