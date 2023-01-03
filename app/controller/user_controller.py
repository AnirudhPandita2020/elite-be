from fastapi import Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from app.database.database_engine import get_db
from app.dto.user_dto import *

router = InferringRouter(tags=["User Controller"])


@cbv(router)
class UserController:
    db: Session = Depends(get_db)

    @router.post(path="/api/elite/create", status_code=status.HTTP_201_CREATED)
    async def create_user(self, create_user_dto: CreateUserDto):
        """Creates a new Elite User"""
        pass

    @router.post(path="/api/elite/login", status_code=status.HTTP_202_ACCEPTED)
    async def login_user(self, user_creds: OAuth2PasswordRequestForm = Depends()):
        """Logs in a user with a working token"""
        pass


