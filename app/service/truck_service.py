import shutil

from fastapi import UploadFile
from openpyxl import load_workbook

from app.exceptions.truck_exceptions import *
from app.exceptions.user_exceptions import *
from app.models.user_model import User
from app.service.repository.truck_repository import *
from app.utils.env_utils import setting


async def add_truck(create_truck: CreateTruckDto, db: Session, user: User) -> Truck:
    if user.isActive and user.authority_level == int(setting.authority_level):
        raise UserAccessDeniedException()

    new_truck = Truck(**create_truck.dict())
    new_truck.created_by = user.id
    save(new_truck, db)
    return new_truck


async def fetch_truck_by_id(truck_id: int, db: Session) -> Truck:
    truck = findTruckById(truck_id, db)
    if not truck:
        raise TruckNotPresentException()
    return truck


async def fetch_truck_by_site(site: Sites, db: Session) -> List[Truck]:
    return findTrucksBySite(site, db)


async def upload_excel_file_of_trucks(file: UploadFile, user: User, db: Session) -> dict:
    with open(f'elite_truck.xlsx', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    truck_list = await fetchTruckFromExcel(load_workbook(file.filename))
    saveTruckList(truck_list, db)
    return {'message': f'Added {len(truck_list)} trucks'}
