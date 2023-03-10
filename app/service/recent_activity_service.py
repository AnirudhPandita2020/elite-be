from typing import List

from firebase_admin import storage
from sqlalchemy.orm import Session

from app.models.certificate_model import Certificates
from app.models.recent_activity_model import RecentActivity
from app.models.truck_model import Truck
from app.service.repository.recent_activity_repository import save, fetch_five_latest_activity
from app.service.repository.truck_repository import findTruckById
from app.service.repository.user_repository import findById
from app.utils.env_utils import setting


async def add_user_activity(name: str, db: Session):
    action = setting.allowed_action[0]
    recent_activity = RecentActivity()
    recent_activity.activity_type = action
    recent_activity.done_by = name
    recent_activity.work_on = 'none'
    save(recent_activity, db)


async def add_truck_activity(truck: Truck, db: Session, action: str):
    recent_activity = RecentActivity()
    recent_activity.activity_type = action
    recent_activity.done_by = findById(truck.created_by, db).email
    recent_activity.work_on = truck.trailer_number
    save(recent_activity, db)


async def add_certificate_activity(certificate: Certificates, db: Session):
    action = setting.allowed_action[1]
    recent_activity = RecentActivity()
    recent_activity.activity_type = action
    truck = findTruckById(certificate.truck_id, db)
    recent_activity.done_by = findById(truck.created_by, db).email
    recent_activity.work_on = f'{certificate.type} ${truck.trailer_number}'
    save(recent_activity, db)


async def get_five_recent_activity(db: Session):
    return fetch_five_latest_activity(db)


async def delete_truck_activity(email: str, trailer_number: str, db: Session):
    action = setting.allowed_action[2]
    recent_activity = RecentActivity()
    recent_activity.activity_type = action
    recent_activity.done_by = email
    recent_activity.work_on = trailer_number
    save(recent_activity, db)


async def delete_certificate_activity(email: str, trailer_number: str, certificate_type: str, db: Session):
    action = setting.allowed_action[2]
    recent_activity = RecentActivity()
    recent_activity.activity_type = action
    recent_activity.done_by = email
    recent_activity.work_on = f'{certificate_type} ${trailer_number}'
    save(recent_activity, db)


async def clear_certificate_from_storage(file_name_list: List[str], db: Session, trailer_number: str):
    storage_bucket = storage.bucket()
    file_blob_list = []
    for file in file_name_list:
        file_blob_list.append(storage_bucket.blob(file))

    storage_bucket.delete_blobs(file_blob_list)

    action = setting.allowed_action[2]
    recent_activity = RecentActivity()
    recent_activity.activity_type = action
    recent_activity.done_by = "System"
    recent_activity.work_on = f"Certificates {trailer_number}"
    save(recent_activity, db)
