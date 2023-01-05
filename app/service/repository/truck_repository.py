from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dto.truck_dto import *
from app.models.truck_model import Truck
from app.utils.enums import Sites


def save(truck: CreateTruckDto, db: Session):
    try:
        db.add(truck)
        db.commit()
        db.refresh(truck)
    except IntegrityError:
        db.rollback()


def findTrucksBySite(sites: Sites, db: Session) -> List[Truck]:
    return db.query(Truck).filter(Truck.site == sites.value).all()


def findTruckByTrailerNumber(trailer_number: str, db: Session) -> Truck:
    return db.query(Truck).filter(Truck.trailer_number == trailer_number).one_or_none()


def findTruckById(truck_id: int, db: Session) -> Truck:
    return db.query(Truck).filter(Truck.truck_id == truck_id).one_or_none()


def saveTruckList(truck_list: List[Truck], db: Session):
    pass


async def fetchTruckFromExcel(file) -> List[Truck]:
    pass
