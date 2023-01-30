from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.database.database_engine import get_db
from app.dto.certificate_dto import CertificateResponse
from app.exceptions.handler.route_handler import RouteErrorHandler
from app.security.oauth2_bearer import get_user_from_token
from app.service.certificate_service import *

router = InferringRouter(tags=["Certificate Controller"], route_class=RouteErrorHandler)


@cbv(router)
class CertificateController:
    db: Session = Depends(get_db)
    user: User = Depends(get_user_from_token)

    @router.post(path="/api/elite/certificate/upload", status_code=status.HTTP_201_CREATED)
    async def upload_certificate_for_truck(self, truck_id: str, file: UploadFile, certificate_type: CertificateEnum,
                                           validity: str, recent_activity: BackgroundTasks):
        """Upload Certificates based on the following types"""
        return await upload_certificate(int(truck_id), file, certificate_type, validity, self.db, self.user,
                                        recent_activity)

    @router.get(path="/api/elite/certificate/fetch", status_code=status.HTTP_200_OK,
                response_model=List[CertificateResponse])
    async def fetch_certificate(self, truck_id: str):
        """Fetch a trucks particular certificate"""
        return await fetch_certificate_of_truck(int(truck_id), self.db)

    @router.get(path="/api/elite/certificate/type", status_code=status.HTTP_200_OK)
    async def fetch_certificates_based_on_type(self, truck_id: str, certificate_type: CertificateEnum):
        """Fetches certificate of a particular type"""
        return await fetch_certificate_site_based(int(truck_id), certificate_type, self.db)

    @router.get(path="/api/elite/certificate/latest", status_code=status.HTTP_200_OK)
    async def fetch_latest_certificate_of_truck(self, truck_id: str):
        """Fetches the latest certificate of all category for a given trailer number"""
        return await fetch_latest_updated_on(int(truck_id), self.db)

    @router.delete(path="/api/elite/certificate/remove", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_certificate(self, truck_id: str, certificate_type: CertificateEnum,
                                 recent_activity_task: BackgroundTasks):
        """Deletes a particular certificate"""
        return await delete_certificate(int(truck_id), self.user.email, certificate_type, self.db, recent_activity_task)
