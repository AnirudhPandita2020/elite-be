from sqlalchemy import TIMESTAMP, Column, Integer, String, text, Boolean

from app.database.database_engine import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    authority_level = Column(Integer, nullable=False, server_default='0')
    is_active = Column(Boolean, server_default='False')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

