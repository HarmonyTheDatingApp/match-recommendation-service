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
  registered_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
  
  tracks = relationship("Track", back_populates="users", cascade="all, delete")


class Track(Base):
  __tablename__ = 'tracks'
  
  id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
  user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"))
  track = sa.Column(sa.String(length=40), nullable=False)
  
  users = relationship("User", back_populates="tracks")
