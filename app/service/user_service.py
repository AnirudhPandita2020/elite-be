import os
import shutil

from fastapi import BackgroundTasks, UploadFile
from firebase_admin import storage

from app.dto.user_dto import *
from app.exceptions.user_exceptions import *
from app.security.oauth2_bearer import *
from app.service.recent_activity_service import add_user_activity
from app.service.repository.user_repository import *
from app.utils.password_utils import *
from app.utils.valid_email import check_valid_company_email
from app.utils.valid_password import check_strong_password


async def create_user(user: CreateUserDto, recent_activity_task: BackgroundTasks, db: Session) -> User:
    if not check_valid_company_email(user.email):
        raise NotValidEmailException()
    if not check_strong_password(user.password):
        raise UserPasswordWeakException()
    existing_user = findByEmail(user.email, db)
    if existing_user:
        raise UserAlreadyPresentException()
    new_user = User(**user.dict())
    new_user.password = hash_password(new_user.password)
    save(new_user, db)
    recent_activity_task.add_task(add_user_activity, name=new_user.name, db=db)
    return new_user


async def login_user(username: str, password: str, db: Session) -> dict:
    if not check_valid_company_email(username):
        raise NotValidEmailException()
    user = findByEmail(username, db)
    if not user or not verify_password(password, user.password):
        raise UserCredentialException()

    access_token = create_bearer_token(data={'user_id': user.id})
    return {'access_token': access_token, 'type': 'bearer'}


async def upload_profile_pic(user: User, db: Session, profile_picture: UploadFile):
    if "image/" not in profile_picture.content_type:
        raise InvalidProfilePhotoException()
    formatted_profile_name = f'{user.email}.{profile_picture.filename.split(".")[1]}'
    with open(formatted_profile_name, 'wb') as file_buffer:
        shutil.copyfileobj(profile_picture.file, file_buffer)

    storage_bucket = storage.bucket()
    profile_blob = storage_bucket.blob(formatted_profile_name)
    profile_blob.upload_from_filename(formatted_profile_name)
    profile_blob.make_public()
    os.unlink(formatted_profile_name)
    addProfileUrl(profile_blob.public_url, db, user)

    return {'message': "Profile photo added"}


async def fetch_user_list(user: User, db: Session):
    return fetchUserList(user, db)


async def change_active_user(db: Session, email: str):
    user = findByEmail(email, db)
    if user is None:
        raise UserEmailNotFoundException()

    if user.role == setting.master_role:
        raise UserAccessDeniedException()

    if not user.is_active:
        updateActiveStatus(email, not user.is_active, int(setting.authority_level), db, setting.main_role)

    else:
        updateActiveStatus(email, not user.is_active, 0, db, setting.default_role)

    return {'message': f'{email} has now been activated'} if user.is_active else {'message': f'{email} is disabled'}
