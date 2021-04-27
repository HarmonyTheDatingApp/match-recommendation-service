from sqlalchemy.orm import Session
from datetime import datetime

from . import models, schemas

def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()

def get_tracks_for_user(db: Session, user_id: int):
  tracks = db.query(models.Track.track).filter(models.Track.user_id == user_id).all()
  return [track.track for track in tracks]

def register_user(db: Session, user: schemas.User):
  new_user = models.User(id=user.id, gender=user.gender, dob=user.dob, pref_interested_in=user.pref_interested_in)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def add_track(db: Session, track: schemas.Track, user_id: int):
  new_track = models.Track(track=track.track, user_id=user_id)
  db.add(new_track)
  db.commit()
  db.refresh(new_track)
  return new_track
