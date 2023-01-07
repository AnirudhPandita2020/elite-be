from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.database.database_engine import get_db
from app.exceptions.handler.route_handler import RouteErrorHandler
from app.models.user_model import User
from app.security.oauth2_bearer import get_user_from_token
from app.service.certificate_service import *

router = InferringRouter(tags=["Certificate Controller"])


@cbv(router)
class CertificateController:
    db: Session = Depends(get_db)
    user: User = Depends(get_user_from_token)

    @router.post(path="/api/elite/certificate/upload", status_code=status.HTTP_201_CREATED)
    async def upload_certificate_for_truck(self, truck_id: str, file: UploadFile, certificate_type: CertificateEnum):
        """Upload Certificates based on the following types"""
        return await upload_certificate(int(truck_id), file, certificate_type, self.db)

    @router.get(path="/api/elite/certificate/fetch", status_code=status.HTTP_200_OK)
    async def fetch_certificate(self, truck_id: str, certificate_type: CertificateEnum):
        """Fetch a trucks particular certificate"""
        pass

    @router.put(path="/api/elite/certificate/update", status_code=status.HTTP_200_OK)
    async def upload_updated_certificate(self):
        """Updates the certificate of a particular truck"""
        pass
