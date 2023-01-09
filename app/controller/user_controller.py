from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.exceptions.handler.route_handler import RouteErrorHandler
from app.service.user_service import *

router = InferringRouter(tags=["User Controller"], route_class=RouteErrorHandler)


@cbv(router)
class UserController:
    db: Session = Depends(get_db)

    @router.post(path="/api/elite/create", status_code=status.HTTP_201_CREATED, response_model=UserModel)
    async def create_user(self, create_user_dto: CreateUserDto):
        """Creates a new Elite User"""
        return await create_user(create_user_dto, self.db)

    @router.post(path="/api/elite/login", status_code=status.HTTP_201_CREATED)
    async def login_user(self, user_creds: OAuth2PasswordRequestForm = Depends()) -> dict:
        """Logs in a user with a working token"""
        return await login_user(user_creds.username, user_creds.password, self.db)
