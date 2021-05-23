from enum import Enum
from pydantic import BaseModel, validator
import datetime
from typing import List

class Gender(str, Enum):
  male = "male"
  female = "female"
  non_binary = "non_binary"

class InterestedIn(str, Enum):
  male = "male"
  female = "female"
  everyone = "everyone"


class Preferences(BaseModel):
  pref_interested_in: InterestedIn
  pref_age_min: int
  pref_age_max: int
  pref_distance: int
  
  @validator('pref_age_min')
  def minimum_age(cls, v):
    if v < 18:
      raise ValueError("Minimum age should be 18.")
    return v
  
  @validator("pref_age_max")
  def age_range(cls, v, values):
    if 'pref_age_min' in values and v < values['pref_age_min']:
      raise ValueError("Age range is invalid.")
    return v
  
  @validator("pref_distance")
  def distance_range(cls, v):
    if v < 4:
      raise ValueError("Minimum distance that can be set is 4 km.")
    if v > 200:
      raise ValueError("Maximum distance can be 200. Consider using passport feature for long distance range.")
    return v
  
  class Config:
    orm_mode = True


class Coordinates(BaseModel):
  long: float
  lat: float
  
  @validator('long')
  def longitude_range(cls, v):
    if not (-180 <= v <= 180):
      raise ValueError("Longitude should be in range [-180, 180]")
    return v
  
  @validator('lat')
  def latitude_range(cls, v):
    if not (-90 <= v <= 90):
      raise ValueError("Latitude should be in range [-90, 90]")
    return v
  
  class Config:
    orm_mode = True


class User(Preferences):
  id: str
  gender: Gender
  dob: datetime.date
  location: Coordinates
  
  class Config:
    orm_mode = True


class UserCreate(User):
  tracks: List[str]

  @validator('tracks')
  def tracks_length(cls, v):
    if len(v) < 4:
      raise ValueError("Length of tracks must be greater than equal to 4.")
    return v


class Track(BaseModel):
  track: str
  
  class Config:
    orm_mode = True


class MusicTaste(BaseModel):
  taste: List[List[float]]
  
  class Config:
    orm_mode = True


class RecommendedUsers(BaseModel):
  recommendation: List[str]

  class Config:
    orm_mode = True


class RightSwipedUsers(BaseModel):
  swipees: List[str]
  
  class Config:
    orm_mode = True


class RightSwipeStats(BaseModel):
  right_swipes: int
  earliest_right_swipe: datetime.datetime

  class Config:
    orm_mode = True
