from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dto.truck_dto import *
from app.models.truck_model import Truck
from app.utils.enums import Sites


def save(truck: Truck, db: Session):
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


def saveTruckList(truck_list: List[Truck], db: Session) -> List[Truck]:
    try:
        for truck in truck_list:
            db.add(truck)
            db.commit()
            db.refresh(truck)
        return truck_list
    except IntegrityError:
        db.rollback()


def fetchTruckFromExcel(file, user_id: int) -> List[Truck]:
    truck_list: List[Truck] = []
    main_sheet = file.active
    rows = main_sheet.max_row
    for i in range(5, rows + 1):
        new_truck = Truck()
        new_truck.trailer_number = main_sheet.cell(row=i, column=2).value
        new_truck.chasis_number = main_sheet.cell(row=i, column=3).value
        new_truck.engine_number = str(main_sheet.cell(row=i, column=3).comment)
        new_truck.suspension = main_sheet.cell(row=i, column=13).value
        new_truck.site = main_sheet.cell(row=i, column=5).value
        new_truck.trailer_length = str(main_sheet.cell(row=i, column=4).comment)
        new_truck.created_by = user_id
        truck_list.append(new_truck)
    return truck_list


def updateTruckDetail(truck_id: int, truck_dto: CreateTruckDto, db: Session) -> Truck:
    try:
        db.query(Truck).filter(Truck.truck_id == truck_id).update(truck_dto.dict(), synchronize_session=False)
        db.commit()
        return findTruckById(truck_id, db)
    except IntegrityError:
        db.rollback()
