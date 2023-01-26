from sqlalchemy import Column, String, TEXT

from app.database.database_engine import Base


class Notification(Base):
    __tablename__ = "notification_token"
    email_id = Column(String, nullable=False, unique=True, primary_key=True)
    token = Column(TEXT, nullable=False)
