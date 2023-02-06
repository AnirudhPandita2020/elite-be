from typing import List

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.exceptions.handler.route_handler import RouteErrorHandler
from app.service.recent_activity_service import get_five_recent_activity
from app.service.user_service import *

router = InferringRouter(tags=["User Controller"], route_class=RouteErrorHandler)


@cbv(router)
class UserController:
    db: Session = Depends(get_db)

    @router.post(path="/api/elite/create", status_code=status.HTTP_201_CREATED, response_model=UserModel)
    async def create_user(self, create_user_dto: CreateUserDto, recent_activity_task: BackgroundTasks):
        """Creates a new Elite User"""
        return await create_user(create_user_dto, recent_activity_task, self.db)

    @router.post(path="/api/elite/login", status_code=status.HTTP_201_CREATED)
    async def login_user(self, user_creds: OAuth2PasswordRequestForm = Depends()) -> dict:
        """Logs in a user with a working token"""
        return await login_user(user_creds.username, user_creds.password, self.db)

    @router.get(path="/api/elite/user/fetch", status_code=status.HTTP_200_OK, response_model=UserModel)
    async def fetch_user_detail(self, user: User = Depends(get_user_from_token)):
        return user

    @router.get(path="/api/elite/user/recent", status_code=status.HTTP_200_OK)
    async def recent_activity(self, user: User = Depends(get_user_from_token)):
        """Fetch 5 recent activity done."""
        return await get_five_recent_activity(self.db)

    @router.post(path="/api/elite/user/profile", status_code=status.HTTP_201_CREATED)
    async def upload_profile_picture(self, profile_picture: UploadFile, user: User = Depends(get_user_from_token)):
        """Upload a profile picture for user"""
        return await upload_profile_pic(user, self.db, profile_picture)

    @router.put(path="/api/elite/user/access", status_code=status.HTTP_200_OK)
    async def provide_access_to_user(self, email: str, user: User = Depends(get_user_from_token)):
        """Provide access to a user (Drive > Manager)"""
        return await change_active_user(self.db, email)

    @router.get(path="/api/elite/user/all", status_code=status.HTTP_200_OK, response_model=List[UserModel])
    async def get_user_list(self, user: User = Depends(get_user_from_token)):
        """Fetch List of user apart from the current one"""
        return await fetch_user_list(user, self.db)
