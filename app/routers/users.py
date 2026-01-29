from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix = "/sqlalchemy/users", tags = ["Users"])

@router.get("/{id}", response_model = schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.ID == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, details = f"User with id: {id} does not exist")
    
    return user

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_user_ORM(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password - user.password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    # Hash the password - user.password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user