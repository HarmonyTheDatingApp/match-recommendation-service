from geoalchemy2.shape import to_shape

from api import models, schemas

def user_model_to_schema(user: models.User):
  loc = to_shape(user.location)
  
  return schemas.User(
    id=user.id,
    gender=user.gender,
    dob=user.dob,
    location=schemas.Coordinates(long=loc.x, lat=loc.y),
    pref_interested_in=user.pref_interested_in,
    pref_age_min=user.pref_age_min,
    pref_age_max=user.pref_age_max,
    pref_distance=user.pref_distance,
  )
