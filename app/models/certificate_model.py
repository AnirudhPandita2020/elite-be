from sqlalchemy import Column, String, Integer, ForeignKey, DATE

from app.database.database_engine import Base


class Certificates(Base):
    __tablename__ = "certificates"
    certificate_id = Column(String, nullable=False, primary_key=True)
    truck_id = Column(Integer, ForeignKey("truck.truck_id", ondelete="CASCADE"), nullable=False)
    road_tax = Column(String, nullable=True)
    road_updated_on = Column(DATE, nullable=True)
    fitness_certificate = Column(String, nullable=True)
    fitness_updated_on = Column(DATE, nullable=True)
    goods_carrier_permission = Column(String, nullable=True)
    goods_updated_on = Column(DATE, nullable=True)
    permit = Column(String, nullable=True)
    permit_updated_on = Column(DATE, nullable=True)
    green_tax = Column(String, nullable=True)
    green_updated_on = Column(DATE, nullable=True)
    insurance = Column(String, nullable=True)
    insurance_updated_on = Column(DATE, nullable=True)


class CertificateHistory(Base):
    __tablename__ = 'certificate_history'
    history_id = Column(Integer, autoincrement=True, primary_key=True)
    certificate_type = Column(String, nullable=False)
    certificate_link = Column(String, nullable=False)
    truck_id = Column(String, ForeignKey('truck.truck_id', ondelete="CASCADE"), nullable=False)
