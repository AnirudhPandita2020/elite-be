from fastapi import BackgroundTasks

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
