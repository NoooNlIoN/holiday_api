from sqlalchemy import Integer, Column, Date, String, Boolean
from models.base import Base
from sqlalchemy.dialects.postgresql import ARRAY


class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    name = Column(String, nullable=False, unique=True)
    states = Column(ARRAY(String), nullable=True)
    type = Column(String, nullable=True)
    is_custom = Column(Boolean, default=False)
