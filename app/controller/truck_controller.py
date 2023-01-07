from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.database.database_engine import get_db
from app.exceptions.handler.route_handler import RouteErrorHandler
from app.security.oauth2_bearer import get_user_from_token
from app.service.truck_service import *

router = InferringRouter(tags=["Truck Controller"], route_class=RouteErrorHandler)


@cbv(router)
class TruckController:
    db: Session = Depends(get_db)
    user: User = Depends(get_user_from_token)

    @router.post(path="/api/elite/truck/add", status_code=status.HTTP_201_CREATED)
    async def add_new_truck(self, create_truck_dto: CreateTruckDto):
        """Enter a new Truck details.Each truck will have its own certification"""
        print(self.user.is_active)
        return await add_truck(create_truck_dto, self.db, self.user)

    @router.get(path="/api/elite/truck/fetch", status_code=status.HTTP_200_OK)
    async def fetch_truck(self, truck_id: str):
        """Fetch a Particular Truck detail"""
        return await fetch_truck_by_id(int(truck_id), self.db)

    @router.put(path="/api/elite/truck/update", status_code=status.HTTP_200_OK)
    async def update_truck(self, truck_id: str, truck_dto: CreateTruckDto):
        """Updates the data of a particular truck id"""
        return await update_truck_detail(int(truck_id), truck_dto, self.user, self.db)

    @router.post(path="/api/elite/truck/upload", status_code=status.HTTP_201_CREATED)
    def upload_truck_excel(self, upload_excel: UploadFile):
        """Upload an Excel file with the truck data"""
        return {'message': 'Upload will be allowed once the excel format is validated by Kuldeep Pandita'}
        # return upload_excel_file_of_trucks(upload_excel, self.user, self.db)

    @router.get(path="/api/elite/truck/site", status_code=status.HTTP_200_OK)
    async def fetch_trucks_based_on_sites(self, site: Sites):
        """Fetch list of trucks based on the site"""
        return await fetch_truck_by_site(site, self.db)
