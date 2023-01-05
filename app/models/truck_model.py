from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey

from app.database.database_engine import Base


class Truck(Base):
    __tablename__ = "truck"
    site = Column(String, nullable=False)
    truck_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    trailer_number = Column(String, unique=True, nullable=False)
    chasis_number = Column(String, unique=True, nullable=False)
    engine_number = Column(String, unique=True, nullable=False)
    trailer_length = Column(Integer, nullable=False)
    suspension = Column(String, nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
