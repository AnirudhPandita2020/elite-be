from fastapi import Depends, status, Header
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from app.database.database_engine import get_db
from app.exceptions.handler.route_handler import RouteErrorHandler
from app.models.user_model import User
from app.security.oauth2_bearer import get_user_from_token
from app.service.notification_service import save_token

router = InferringRouter(tags=['Notification Controller'], route_class=RouteErrorHandler)


@cbv(router)
class NotificationController:
    user: User = Depends(get_user_from_token)
    db: Session = Depends(get_db)

    @router.post(path="/api/elite/notification", status_code=status.HTTP_200_OK)
    async def save_notification_token(self, token: str = Header(...)):
        """Stores the notification for FCM Push Notification"""
        return await save_token(token, self.user, self.db)
