import shutil

from fastapi import UploadFile
from firebase_admin import storage

from app.exceptions.certificate_exceptions import *
from app.service.repository.certificate_repository import *
from app.utils.enums import CertificateEnum


async def upload_certificate(truck_id: int, certificate_file: UploadFile, certificate_type: CertificateEnum,
                             db: Session):
    print(await fetch_url_of_certificate(file=certificate_file))


async def fetch_certificate(truck_id, certificate_type: CertificateEnum):
    pass


async def upload_updated_certificate(certificate_id: str, certificate_type: CertificateEnum):
    pass


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

    return file_blob.public_url
