from typing import List

from fastapi import Response, status, HTTPException, APIRouter
from .. import schemas
from ..database import conn, cur

router = APIRouter(prefix = "", tags = ["Old"])

@router.get("/")
def root():
    return {"message": "Hello World"}

@router.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    return {"data": posts}

@router.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate):
    cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cur.fetchone()

    conn.commit()
    return {"data": new_post}

@router.get("/posts/{id}")
def get_post(id: int):
    cur.execute("""SELECT * FROM posts WHERE "ID" = %s""", (str(id),))
    post = cur.fetchone() 
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} was not found')
    return {"post_detail": post}

@router.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cur.execute("""DELETE FROM posts WHERE "ID" = %s RETURNING * """, (str(id),))
    deleted_post = cur.fetchone()

    if deleted_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} doesn\'t exist')
    
    conn.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}")
def update_posts(id: int, post: schemas.PostCreate):
    cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE "ID" = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    updated_post = cur.fetchone()
    if updated_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} doesn\'t exist')
    
    conn.commit()
    return {'data': updated_post}
