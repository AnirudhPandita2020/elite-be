import datetime
import os
import shutil
from datetime import date

from fastapi import UploadFile, BackgroundTasks
from firebase_admin import storage

from app.exceptions.certificate_exceptions import *
from app.exceptions.truck_exceptions import TruckNotPresentException
from app.exceptions.user_exceptions import UserAccessDeniedException
from app.models.truck_model import Truck
from app.models.user_model import User
from app.service.recent_activity_service import add_certificate_activity, delete_certificate_activity
from app.service.repository.certificate_repository import *
from app.service.repository.truck_repository import findTruckById
from app.service.truck_service import fetch_truck_by_id
from app.utils.certificate_id_generator import certificate_id
from app.utils.enums import CertificateEnum
from app.utils.env_utils import setting


async def upload_certificate(truck_id: int, certificate_file: UploadFile, certificate_type: CertificateEnum,
                             validity: str, db: Session, user: User, recent_activity: BackgroundTasks):
    if user.is_active is False or user.authority_level != int(setting.authority_level):
        raise UserAccessDeniedException()

    if findTruckById(truck_id, db) is None:
        raise TruckNotPresentException()

    latest_certificate = fetch_latest_certificate_by_type(truck_id, certificate_type.value, db)
    if len(latest_certificate) != 0 and datetime.datetime.strptime(validity, "%Y-%m-%d").date() < latest_certificate[
        0].validity_till:
        raise CertificateValidityException()

    new_certificate = Certificates()
    new_certificate.validity_till = datetime.datetime.strptime(validity, "%Y-%m-%d").date()
    new_certificate.certificate_id = certificate_id()
    truck = await fetch_truck_by_id(truck_id, db)
    new_certificate.certificate_link = await fetch_url_of_certificate(certificate_file,
                                                                      truck,
                                                                      certificate_type.value, validity)
    new_certificate.certificate_file_name = f'{truck.trailer_number}_{certificate_type.value}_{validity}.pdf'
    new_certificate.truck_id = truck_id
    new_certificate.updated_on = date.today()
    new_certificate.type = certificate_type.value
    save(new_certificate, db)
    recent_activity.add_task(add_certificate_activity, certificate=new_certificate, db=db)
    return new_certificate


async def fetch_certificate_of_truck(truck_id: int, db: Session):
    return fetch_certificate_based_on_truck_id(truck_id, db)


async def fetch_url_of_certificate(file: UploadFile, truck: Truck, certificate_type: str, validity: str):
    if file.content_type != "application/pdf":
        raise CertificateFormatException()

    formatted_file_name = f'{truck.trailer_number}_{certificate_type}_{validity}.pdf'
    with open(formatted_file_name, 'wb') as file_buffer:
        shutil.copyfileobj(file.file, file_buffer)

    storage_bucket = storage.bucket()
    file_blob = storage_bucket.blob(formatted_file_name)
    file_blob.upload_from_filename(formatted_file_name)
    file_blob.make_public()
    os.unlink(formatted_file_name)
    return file_blob.public_url


async def fetch_certificate_site_based(truck_id: int, certificate_type: CertificateEnum, db: Session) -> List[
    Certificates]:
    certificate = fetch_certificate_by_truck_id_and_type(truck_id, certificate_type.value, db)
    if certificate is None:
        raise CertificateNotPresentException()

    return certificate


async def fetch_latest_certificate_for_all_trucks(truck_id: int, db: Session):
    return fetch_latest_certificate_of_all_type(truck_id, db)


async def fetch_latest_updated_on(truck_id: int, db: Session):
    return fetch_latest_certificate_of_all_type(truck_id, db)


async def delete_certificate(truck_id: int, email: str, certificate_type: CertificateEnum, db: Session,
                             recent_activity_task: BackgroundTasks):
    certificate_list = fetch_certificate_by_truck_id_and_type(truck_id, certificate_type.value, db)
    if len(certificate_list) == 0:
        raise CertificateNotPresentException()

    # deleting those files from firebase as well
    file_names = [certificate.certificate_file_name for certificate in certificate_list if
                  certificate.certificate_file_name is not None]

    storage_bucket = storage.bucket()
    file_blob_list = []
    for file in file_names:
        file_blob_list.append(storage_bucket.blob(file))

    storage_bucket.delete_blobs(file_blob_list)
    recent_activity_task.add_task(delete_certificate_activity, email=email,
                                  trailer_number=findTruckById(truck_id, db).trailer_number,
                                  certificate_type=certificate_type.value, db=db)
