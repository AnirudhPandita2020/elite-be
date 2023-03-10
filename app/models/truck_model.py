from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey, TEXT, Boolean

from app.database.database_engine import Base


class Truck(Base):
    __tablename__ = "truck"
    site = Column(String, nullable=False)
    truck_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    trailer_number = Column(String, unique=True, nullable=False)
    trailer_info = Column(String, nullable=False)
    chasis_number = Column(String, unique=True, nullable=False)
    engine = Column(String, nullable=True)
    engine_number = Column(String, unique=True, nullable=False)
    trailer_length = Column(String, nullable=True)
    suspension = Column(String, nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    certificate_disabled = Column(TEXT, nullable=True)
    is_active = Column(Boolean, server_default='True')
