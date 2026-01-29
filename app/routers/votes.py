from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix = "/sqlalchemy/votes", tags = ["Votes"])

@router.get("/{id}", response_model = schemas.VoteResponse)
def get_post_votes(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.ID == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")
    
    votes = db.query(models.Vote).filter(models.Vote.post_ID == id).count()


    return schemas.VoteResponse(post_ID = id, votes_number = votes)

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.ID == vote.post_ID).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {vote.post_ID} does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_ID == vote.post_ID, models.Vote.user_ID == user_id.ID)
    found_vote = vote_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"Post with id: {vote.post_ID} already voted by user: {user_id.ID}")
        new_vote = models.Vote(post_ID = vote.post_ID, user_ID = user_id.ID)
        db.add(new_vote)
        db.commit()
        
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {vote.post_ID} yet not voted by user: {user_id.ID}")
        vote_query.delete(synchronize_session = False)
        db.commit()

        return {"message": "successfully removed vote"}