from enum import Enum
from pydantic import BaseModel
import datetime

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


class Track(BaseModel):
  track: str
  
  class Config:
    orm_mode = True
