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
  
  class Config:
    orm_mode = True


class User(Preferences):
  id: int
  gender: Gender
  dob: datetime.date
  
  class Config:
    orm_mode = True


class UserCreate(User):
  tracks: List[str]


class Track(BaseModel):
  track: str
  
  class Config:
    orm_mode = True


class MusicTaste(BaseModel):
  taste: List[List[float]]
  
  class Config:
    orm_mode = True


class RecommendedUsers(BaseModel):
  recommendation: List[int]

  class Config:
    orm_mode = True


class RightSwipedUsers(BaseModel):
  swipees: List[int]
  
  class Config:
    orm_mode = True


class RightSwipeStats(BaseModel):
  right_swipes: int
  earliest_right_swipe: datetime.datetime

  class Config:
    orm_mode = True
