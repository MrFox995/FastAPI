from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .routers import posts, users, old, auth, votes

### ORM PART ###
# OLD: models.Base.metadata.create_all(bind = engine) -> Obsolete after inplementing Alembic
### ORM PART ###

app = FastAPI()

### CORS ###
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
### CORS ###

##################################### ROUTERS ##################################### 
app.include_router(old.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(votes.router)
app.include_router(auth.router)
##################################### ROUTERS ##################################### 