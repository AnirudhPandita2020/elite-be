from fastapi import Depends, status, Header
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from app.database.database_engine import get_db
from app.exceptions.handler.route_handler import RouteErrorHandler
from app.models.user_model import User
from app.security.oauth2_bearer import get_user_from_token

router = InferringRouter(tags=['Admin Controller'], route_class=RouteErrorHandler)


@cbv(router)
class AdminController:
    db: Session = Depends(get_db)
    user: User = Depends(get_user_from_token)

    @router.delete(path="/api/admin/data/clear", status_code=status.HTTP_200_OK)
    async def clear_truck_database(self, api_key: str = Header(...)):
        """Clear Truck database"""
        pass

    @router.delete(path="/api/admin/user/delete", status_code=status.HTTP_200_OK)
    async def clear_elite_user(self, api_key: str = Header(...)):
        """Delete Elite User"""
        pass

    @router.get(path="/api/admin/data/excel",status_code=status.HTTP_200_OK)
    async def fetch_data_to_excel(self,api_key: str = Header(...)):
        """Convert data to excel format"""
        pass

