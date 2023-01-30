from typing import List, Tuple

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.certificate_model import *


def fetch_certificate_by_truck_id_and_type(truck_id: int, cer_type: str, db: Session) -> List[Certificates]:
    return db.query(Certificates).filter(Certificates.truck_id == truck_id, Certificates.type == cer_type).order_by(
        Certificates.updated_on.desc()).all()


def fetch_latest_certificate_by_type(truck_id: int, cer_type: str, db: Session) -> List[Certificates]:
    return db.query(Certificates).filter(Certificates.truck_id == truck_id, Certificates.type == cer_type).order_by(
        Certificates.validity_till.desc()).limit(1).all()


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


def fetch_latest_certificate_of_all_type(truck_id, db: Session) -> List[Tuple]:
    return db.query(
        Certificates.type,
        func.max(Certificates.validity_till).label('validity_till')
    ).filter(Certificates.truck_id == truck_id).group_by(Certificates.type).all()


def fetch_latest_updated_certificate(truck_id: int, db: Session):
    return db.query(
        Certificates.type,
        func.max(Certificates.updated_on).label('updated_on')
    ).filter(Certificates.truck_id == truck_id).group_by(Certificates.type).all()


def fetch_certificate_by_id(certificate_id: str, db: Session):
    return db.query(Certificates).filter(Certificates.certificate_id == certificate_id).one_or_none()


def delete_certificate_by_id(certificate_id: str, certificate_type: str, db: Session):
    db.query(Certificates).filter(Certificates.certificate_id == certificate_id,
                                  Certificates.type == certificate_type).delete(synchronize_session=False)
    db.commit()


def fetch_all_certificates_of_truck(truck_id: int, db: Session) -> List[Certificates]:
    return db.query(Certificates).filter(Certificates.truck_id == truck_id).all()
