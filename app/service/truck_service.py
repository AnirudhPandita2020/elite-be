import shutil

from fastapi import BackgroundTasks
from fastapi import UploadFile
from openpyxl import load_workbook

from app.exceptions.truck_exceptions import *
from app.exceptions.user_exceptions import *
from app.models.user_model import User
from app.service.recent_activity_service import add_truck_activity
from app.service.repository.truck_repository import *
from app.utils.env_utils import setting


async def add_truck(create_truck: CreateTruckDto, recent_activity: BackgroundTasks, db: Session, user: User) -> Truck:
    if user.is_active is False and user.authority_level != int(setting.authority_level):
        raise UserAccessDeniedException()
    if create_truck.site not in setting.allowed_sites:
        raise InvalidSiteException(create_truck.site)
    new_truck = Truck(**create_truck.dict())
    new_truck.created_by = user.id
    save(new_truck, db)
    recent_activity.add_task(add_truck_activity, truck=new_truck, db=db, action="ADD")
    return new_truck


async def fetch_truck_by_id(truck_id: int, db: Session) -> Truck:
    truck = findTruckById(truck_id, db)
    if not truck:
        raise TruckNotPresentException()
    return truck


async def fetch_truck_by_site(site: Sites, db: Session) -> List[Truck]:
    return findTrucksBySite(site, db)


async def fetch_truck_by_trailer_number(number: str, db: Session) -> Truck:
    return findByTrailerNumber(number, db)


async def fetch_truckIds_of_site(site: str, db: Session):
    return fetch_truck_id_by_site(site, db)


def upload_excel_file_of_trucks(file: UploadFile, user: User, db: Session):
    if user.is_active is False and user.authority_level != int(setting.authority_level):
        raise UserAccessDeniedException()
    with open(f'elite_truck.xlsx', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    truck_list = fetchTruckFromExcel(load_workbook(f'elite_truck.xlsx'), user.id)
    saveTruckList(truck_list, db)
    return truck_list


async def update_truck_detail(truck_id: int, update_truck_dto: CreateTruckDto, user: User, db: Session,
                              recent_activity: BackgroundTasks) -> Truck:
    if user.is_active is False and user.authority_level != int(setting.authority_level):
        raise UserAccessDeniedException()
    truck = findTruckById(truck_id, db)
    if not truck:
        raise TruckNotPresentException()
    if truck.created_by != user.id:
        raise UserAccessDeniedException()

    truck = updateTruckDetail(truck_id, update_truck_dto, db)
    recent_activity.add_task(add_truck_activity, truck=truck, db=db, action="MODIFY")
    return truck
