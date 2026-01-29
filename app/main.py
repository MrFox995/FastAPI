import psycopg
import time

from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
from psycopg.rows import dict_row

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
                {"title": "title of post 1", "content": "content of post 1", "id": 1},
                {"title": "title of post 2", "content": "content of post 2", "id": 2},
                {"title": "title of post 3", "content": "content of post 3", "id": 3}
            ]

##################################### DB CONNECTION ##################################### 
while True:
    try:
        conn = psycopg.connect(host = 'localhost', dbname = 'fastapi', user = 'postgres', password = 'admin', row_factory = dict_row)
        cur = conn.cursor()
        print("DataBase connection was succesfull!")
        break
    except Exception as error:
        print(f"Connecting to DataBase failsed\nError is: {error}")
        time.sleep(2)
##################################### DB CONNECTION ##################################### 


##################################### FUNCTIONS ##################################### 
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

##################################### FUNCTIONS ##################################### 
        
##################################### REQUESTS ######################################
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cur.fetchone()

    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    cur.execute("""SELECT * FROM posts WHERE "ID" = %s""", (str(id),))
    post = cur.fetchone() 
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} was not found')
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cur.execute("""DELETE FROM posts WHERE "ID" = %s RETURNING * """, (str(id),))
    deleted_post = cur.fetchone()

    if deleted_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} doesn\'t exist')
    
    conn.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE "ID" = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    updated_post = cur.fetchone()
    if updated_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'post with id: {id} doesn\'t exist')
    
    conn.commit()
    return {'data': updated_post}
##################################### REQUESTS ######################################
    



# @app.get("/posts")
# def get_posts():
#     return {"data": "This is your posts"}

# @app.get("/")
# def root():
#     return {"message": "Hello World"}

# ##################################### OLD #####################################
# #@app.post("/createposts")
# #def create_posts(payload: dict = Body(...)):
# #    print(payload)
# #    return {"new_post": f"title: {payload['title']}, content: {payload['content']}"}
# ##################################### OLD #####################################

# @app.post("/createposts")
# def create_posts(post: Post):
#     print(post)
#     print(post.model_dump())
#     print(post.title)
#     print(post.published)
#     return {"data": post}