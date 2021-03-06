from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas, utils
from .database import SessionLocal, engine
from core.Spotify import Spotify

client = Spotify()

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
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db_session)):
  if crud.get_user(db, user_id=user.id):
    raise HTTPException(status_code=400, detail="User already registered.")
  new_user = crud.register_user(db, user=user, spotify_client=client)
  return utils.user_model_to_schema(new_user)

@app.post("/users/{user_id}/preferences/", response_model=schemas.User)
def update_preferences(user_id: str, preferences: schemas.Preferences, db: Session = Depends(get_db_session)):
  user = crud.get_user(db, user_id)
  if user is None:
    return HTTPException(status_code=400, detail="User not found.")
  return utils.user_model_to_schema(crud.post_preferences(db, user, preferences))

@app.post("/users/{user_id}/location/", response_model=schemas.User)
def update_location(user_id: str, location: schemas.Coordinates, db: Session = Depends(get_db_session)):
  user = crud.get_user(db, user_id)
  if user is None:
    return HTTPException(status_code=400, detail="User not found.")
  return utils.user_model_to_schema(crud.update_location(db, user, location))

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: str, db: Session = Depends(get_db_session)):
  user = crud.get_user(db, user_id=user_id)
  if user is None:
    raise HTTPException(status_code=404, detail="User not found.")
  return utils.user_model_to_schema(user)

@app.post("/users/{user_id}/track/", response_model=schemas.Track)
def add_track(track: schemas.Track, user_id: str, db: Session = Depends(get_db_session)):
  return crud.add_track(db, track=track, user_id=user_id)

@app.get("/users/{user_id}/track/", response_model=List[str])
def get_tracks(user_id: str, db: Session = Depends(get_db_session)):
  tracks = crud.get_tracks_for_user(db, user_id=user_id)
  return tracks

@app.get("/users/{user_id}/taste/", response_model=schemas.MusicTaste)
def get_music_taste(user_id: str, db: Session = Depends(get_db_session)):
  return crud.get_music_taste(db, user_id)

@app.get("/users/{user_id}/recommend/", response_model=schemas.RecommendedUsers)
def get_recommendation(user_id: str, long: Optional[float] = None, lat: Optional[float] = None,
                       limit: Optional[int] = 10, db: Session = Depends(get_db_session)):
  """
  If location given, then it updates the user location and then runs the recommendation algorithm.
  """
  if long is None and lat is None:
    location = None
  elif long and lat:
    location = schemas.Coordinates(long=long, lat=lat)
  else:
    raise HTTPException(status_code=400, detail="Both longitude & latitude required.")

  user = crud.get_user(user_id=user_id, db=db)
  if user is None:
    raise HTTPException(status_code=400, detail="User not found.")
  return crud.get_user_recommendation(db, user, location, limit)

@app.post("/users/{user_id}/update-right-swipes/", response_model=schemas.RightSwipeStats)
def post_right_swiped_users(user_id: str, right_swiped_users: schemas.RightSwipedUsers,
                            db: Session = Depends(get_db_session)):
  user = crud.get_user(user_id=user_id, db=db)
  if user is None:
    raise HTTPException(status_code=400, detail="User not found.")
  return crud.post_right_swipes(db, user, right_swiped_users)
