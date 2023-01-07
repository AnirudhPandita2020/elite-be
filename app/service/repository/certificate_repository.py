from sqlalchemy.orm import Session

from app.models.certificate_model import *


def fetch_certificate_by_truck_id(truck_id: int, db: Session) -> Certificates:
    return db.query(Certificates).filter(Certificates.truck_id == truck_id).one_or_none()

