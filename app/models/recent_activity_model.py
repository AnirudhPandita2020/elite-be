from sqlalchemy import Column, Integer, String, text, TIMESTAMP

from app.database.database_engine import Base


class RecentActivity(Base):
    __tablename__ = "recent_activity"
    activity_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    activity_type = Column(String, nullable=False)
    work_on = Column(String, nullable=False)
    done_by = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
