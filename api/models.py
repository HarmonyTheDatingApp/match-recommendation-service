import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .database import Base
from api.schemas import Gender, InterestedIn


class User(Base):
  __tablename__ = "users"
  
  id = sa.Column(sa.Integer, primary_key=True, index=True)
  gender = sa.Column(sa.Enum(Gender, name="gender_enum", create_type=False), nullable=False)
  dob = sa.Column(sa.Date(), nullable=False)
  pref_interested_in = sa.Column(sa.Enum(InterestedIn, name="pref_interested_in_enum",
                                         create_type=False), nullable=False)
  pref_age_min = sa.Column(sa.Integer, nullable=False, default=18)
  pref_age_max = sa.Column(sa.Integer, nullable=False, default=60)
  registered_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
  
  tracks = relationship("Track", back_populates="users", cascade="all, delete")
  tastes = relationship("MusicTaste", back_populates="users", cascade="all, delete")


class Track(Base):
  __tablename__ = 'tracks'
  
  id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
  user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"))
  track = sa.Column(sa.String(length=40), nullable=False)
  
  users = relationship("User", back_populates="tracks")


class MusicTaste(Base):
  __tablename__ = 'musictaste'
  
  id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
  user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"))
  vector = sa.Column(sa.ARRAY(sa.Float), nullable=False)
  created_on = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

  users = relationship("User", back_populates="tastes")


class RightSwipe(Base):
  __tablename__ = 'rightswipes'
  
  id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
  swiper = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  swipee = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  created_on = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
