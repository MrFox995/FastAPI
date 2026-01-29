from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing_extensions import Annotated

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    ID: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    ID: Optional[int] = None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    ID: int
    # owner_ID: int
    owner: UserResponse
    created_at: datetime

    class Config:
        from_attributes = True

class PostResponseV2(BaseModel):
    post: PostResponse
    votes_number: int

    class Config:
        from_attributes = True

class Vote(BaseModel):
    post_ID: int
    dir: Annotated[int, Field(ge = 0, le = 1)]

class VoteResponse(BaseModel):
    post_ID: int
    votes_number: int

