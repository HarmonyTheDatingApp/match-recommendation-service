from enum import Enum
from pydantic import BaseModel
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

class User(BaseModel):
  id: int
  gender: Gender
  dob: datetime.date
  pref_interested_in: InterestedIn
  
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
