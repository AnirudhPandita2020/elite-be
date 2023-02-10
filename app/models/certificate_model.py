from sqlalchemy import Column, String, Integer, ForeignKey, DATE

from app.database.database_engine import Base


class Certificates(Base):
    __tablename__ = "certificates"
    certificate_id = Column(String, nullable=False, primary_key=True)
    truck_id = Column(Integer, ForeignKey("truck.truck_id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    certificate_link = Column(String, nullable=False)
    certificate_file_name = Column(String, nullable=True)
    updated_on = Column(DATE, nullable=False)
    validity_till = Column(DATE, nullable=False)
