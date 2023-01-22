import datetime
import os
import shutil
from datetime import date

from fastapi import UploadFile, BackgroundTasks
from firebase_admin import storage

from app.exceptions.certificate_exceptions import *
from app.exceptions.truck_exceptions import TruckNotPresentException
from app.exceptions.user_exceptions import UserAccessDeniedException
from app.models.user_model import User
from app.service.recent_activity_service import add_certificate_activity
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

    new_certificate = Certificates()
    new_certificate.validity_till = datetime.datetime.strptime(validity, "%Y-%m-%d").date()
    new_certificate.certificate_id = certificate_id()
    new_certificate.certificate_link = await fetch_url_of_certificate(certificate_file,
                                                                      await fetch_truck_by_id(truck_id, db),
                                                                      certificate_type.value, validity)
    new_certificate.truck_id = truck_id
    new_certificate.updated_on = date.today()
    new_certificate.type = certificate_type.value
    save(new_certificate, db)
    recent_activity.add_task(add_certificate_activity, certificate=new_certificate, db=db)
    return new_certificate


async def fetch_certificate_of_truck(truck_id: int, db: Session):
    return fetch_certificate_based_on_truck_id(truck_id, db)


async def fetch_url_of_certificate(file: UploadFile, trailer_number: str, certificate_type: str, validity: str):
    extension = file.filename.split('.')[1]
    if extension != 'pdf':
        raise CertificateFormatException()

    formatted_file_name = f'{trailer_number}_{certificate_type}_{validity}.pdf'
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
