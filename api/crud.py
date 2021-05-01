from sqlalchemy.orm import Session
from datetime import datetime

from . import models, schemas
from core.FeatureExtractor import FeatureExtractor
from core.Spotify import Spotify

def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()

def get_tracks_for_user(db: Session, user_id: int):
  tracks = db.query(models.Track.track).filter(models.Track.user_id == user_id).all()
  return [track.track for track in tracks]

def register_user(db: Session, user: schemas.UserCreate, spotify_client: Spotify) -> schemas.User:
  new_user = models.User(id=user.id, gender=user.gender, dob=user.dob, pref_interested_in=user.pref_interested_in)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  
  tracks = [models.Track(user_id=user.id, track=track) for track in user.tracks]
  db.bulk_save_objects(tracks)
  
  # Enchancement: Can run this extra task on separate worker.
  feature_extractor = FeatureExtractor(track_ids=user.tracks, client=spotify_client)
  cluster_centres = feature_extractor.compute_clusters_in_tracks(Spotify.AUDIO_FEATURES, n_clusters=4)
  tastes = [models.MusicTaste(user_id=user.id, vector=cluster_center) for cluster_center in cluster_centres]
  for taste in tastes:
    db.add(taste)

  db.commit()
  return new_user

def add_track(db: Session, track: schemas.Track, user_id: int):
  new_track = models.Track(track=track.track, user_id=user_id)
  db.add(new_track)
  db.commit()
  db.refresh(new_track)
  return new_track

def get_music_taste(db: Session, user_id: int):
  tastes = db.query(models.MusicTaste.vector).filter(models.MusicTaste.user_id == user_id).all()
  return {'taste': [row[0] for row in tastes]}
