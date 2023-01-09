from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.certificate_model import *


def fetch_certificate_by_truck_id_and_type(truck_id: int, cer_type: str, db: Session) -> Certificates:
    return db.query(Certificates).filter(Certificates.truck_id == truck_id, Certificates.type == cer_type).one_or_none()


def fetch_certificate_based_on_truck_id(truck_id: int, db: Session) -> List[Certificates]:
    return db.query(Certificates).filter(Certificates.truck_id == truck_id).all()


def update_certificate_of_truck(certificate: Certificates, db: Session) -> Certificates:
    db.query(Certificates).filter(Certificates.truck_id == certificate.truck_id).update({
        Certificates.updated_on: certificate.updated_on,
        Certificates.certificate_link: certificate.certificate_link
    }, synchronize_session=False)
    db.commit()
    db.refresh(certificate)
    return certificate


def save(certificate: Certificates, db: Session) -> Certificates:
    try:
        db.add(certificate)
        db.commit()
        db.refresh(certificate)
        return certificate
    except IntegrityError:
        db.rollback()

