import os
import shutil
from datetime import date

from fastapi import UploadFile
from firebase_admin import storage

from app.exceptions.certificate_exceptions import *
from app.exceptions.truck_exceptions import TruckNotPresentException
from app.exceptions.user_exceptions import UserAccessDeniedException
from app.models.user_model import User
from app.service.repository.certificate_repository import *
from app.service.repository.truck_repository import findTruckById
from app.utils.certificate_id_generator import certificate_id
from app.utils.enums import CertificateEnum
from app.utils.env_utils import setting


async def upload_certificate(truck_id: int, certificate_file: UploadFile, certificate_type: CertificateEnum,
                             db: Session, user: User):
    if user.is_active is False or user.authority_level != int(setting.authority_level):
        raise UserAccessDeniedException()

    if findTruckById(truck_id, db) is None:
        raise TruckNotPresentException()

    new_certificate = Certificates()
    new_certificate.certificate_id = certificate_id()
    new_certificate.certificate_link = await fetch_url_of_certificate(certificate_file)
    new_certificate.truck_id = truck_id
    new_certificate.updated_on = date.today()
    new_certificate.type = certificate_type.value
    save(new_certificate, db)
    return new_certificate


async def fetch_certificate_of_truck(truck_id: int, db: Session):
    return fetch_certificate_based_on_truck_id(truck_id, db)


async def fetch_url_of_certificate(file: UploadFile):
    extension = file.filename.split('.')[1]
    if extension != 'pdf':
        raise CertificateFormatException()

    with open(f'{file.filename}', 'wb') as file_buffer:
        shutil.copyfileobj(file.file, file_buffer)

    storage_bucket = storage.bucket()
    file_blob = storage_bucket.blob(file.filename)
    file_blob.upload_from_filename(file.filename)
    file_blob.make_public()
    os.unlink(file.filename)
    return file_blob.public_url


async def fetch_certificate_site_based(truck_id: int, certificate_type: CertificateEnum, db: Session) -> List[Certificates]:
    certificate = fetch_certificate_by_truck_id_and_type(truck_id, certificate_type.value, db)
    if certificate is None:
        raise CertificateNotPresentException()

    return certificate
