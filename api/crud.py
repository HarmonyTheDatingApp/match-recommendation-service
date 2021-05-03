from sqlalchemy.orm import Session
from sqlalchemy import func, extract
import numpy as np
from typing import List
from datetime import datetime

from api import models, schemas
from core.FeatureExtractor import FeatureExtractor
from core.Spotify import Spotify


def get_user(db: Session, user_id: int) -> models.User:
  return db.query(models.User).filter(models.User.id == user_id).first()


def get_tracks_for_user(db: Session, user_id: int):
  tracks = db.query(models.Track.track).filter(models.Track.user_id == user_id).all()
  return [track.track for track in tracks]


def register_user(db: Session, user: schemas.UserCreate, spotify_client: Spotify) -> schemas.User:
  new_user = models.User(
    id=user.id,
    gender=user.gender,
    dob=user.dob,
    pref_interested_in=user.pref_interested_in,
    pref_age_min=user.pref_age_min,
    pref_age_max=user.pref_age_max
  )
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


def post_preferences(db: Session, this_user: models.User, preferences: schemas.Preferences):
  this_user.pref_interested_in = preferences.pref_interested_in
  this_user.pref_age_min = preferences.pref_age_min
  this_user.pref_age_max = preferences.pref_age_max
  db.commit()
  db.refresh(this_user)
  return this_user


def add_track(db: Session, track: schemas.Track, user_id: int):
  new_track = models.Track(track=track.track, user_id=user_id)
  db.add(new_track)
  db.commit()
  db.refresh(new_track)
  return new_track


def get_music_taste(db: Session, user_id: int):
  tastes = db.query(models.MusicTaste.vector).filter(models.MusicTaste.user_id == user_id).all()
  return {'taste': [row[0] for row in tastes]}


def get_user_recommendation(db: Session, this_user: models.User, limit: int = 10):
  # embeddings
  embeddings = np.array([embedding[0] for embedding in
                         db.query(models.MusicTaste.vector).filter(models.MusicTaste.user_id == this_user.id)])
  mean_embedding = np.average(embeddings, axis=0).tolist()
  mean_embedding = ','.join(map(str, mean_embedding))
  
  right_swipes = db.query(models.RightSwipe).filter(models.RightSwipe.swiper == this_user.id).subquery()
  
  recommended_users = db.query(models.MusicTaste.user_id)\
                        .outerjoin(right_swipes, right_swipes.c.swipee == models.MusicTaste.user_id)\
                        .join(models.User, models.MusicTaste.user_id == models.User.id)\
                        .filter(right_swipes.c.swipee == None)\
                        .filter(models.User.id != this_user.id)
  
  # preference filters
  preferred_gender = None if this_user.pref_interested_in == 'everyone' else this_user.pref_interested_in
  if preferred_gender:
    recommended_users = recommended_users.filter(models.User.gender == preferred_gender)
  pref_age_min, pref_age_max = this_user.pref_age_min, this_user.pref_age_max
  recommended_users = recommended_users.filter(
    extract('year', func.age(models.User.dob)).between(pref_age_min, pref_age_max)
  )
  
  recommended_users = recommended_users.group_by(models.MusicTaste.user_id)\
                                       .order_by(func.avg(func.cube(models.MusicTaste.vector)
                                                              .op('<->')(func.cube(mean_embedding))))\
                                       .limit(limit)
  
  return {'recommendation': [int(item[0]) for item in recommended_users.all()]}


def post_right_swipes(db: Session, this_user: models.User, right_swipes: schemas.RightSwipedUsers):
  instances = [models.RightSwipe(swiper=this_user.id, swipee=swipee)
               for swipee in right_swipes.swipees if swipee != this_user.id]
  db.bulk_save_objects(instances)
  db.commit()
  
  total_rt_swipes = db.query(func.count(models.RightSwipe.id)).filter(models.RightSwipe.swiper == this_user.id).first()
  earliest_rt_swipe = db.query(func.max(models.RightSwipe.created_on)) \
                        .filter(models.RightSwipe.swiper == this_user.id).first()
  
  return schemas.RightSwipeStats(right_swipes=total_rt_swipes[0], earliest_right_swipe=earliest_rt_swipe[0])
