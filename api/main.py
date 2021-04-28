from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency (sort of a context manager specifically for FastAPI APIs)
def get_db_session():
  session = SessionLocal()
  try:
    yield session
  finally:
    session.close()

@app.get("/")
def home():
  return {"msg": "Hello world!"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db_session)):
  if crud.get_user(db, user_id=user.id):
    raise HTTPException(status_code=400, detail="User already registered.")
  return crud.register_user(db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db_session)):
  user = crud.get_user(db, user_id=user_id)
  if user is None:
    raise HTTPException(status_code=404, detail="User not found.")
  return user

@app.post("/users/{user_id}/track/", response_model=schemas.Track)
def add_track(track: schemas.Track, user_id: int, db: Session = Depends(get_db_session)):
  return crud.add_track(db, track=track, user_id=user_id)

@app.get("/users/{user_id}/track/", response_model=List[str])
def get_tracks(user_id: int, db: Session = Depends(get_db_session)):
  tracks = crud.get_tracks_for_user(db, user_id=user_id)
  return tracks
