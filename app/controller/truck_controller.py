from fastapi import Depends, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from app.database.database_engine import get_db
from app.models.user_model import User
from app.security.oauth2_bearer import get_user_from_token

router = InferringRouter(tags=["Truck Controller"])


@cbv(router)
class TruckController:
    db: Session = Depends(get_db)
    user: User = Depends(get_user_from_token)

    @router.post(path="/api/elite/truck/add", status_code=status.HTTP_201_CREATED)
    async def add_new_truck(self):
        """Enter a new Truck details.Each truck will have its own certification"""
        pass

    @router.get(path="/api/elite/truck/fetch", status_code=status.HTTP_200_OK)
    async def fetch_truck(self, truck_id: str):
        """Fetch a Particular Truck detail"""
        pass

    @router.put(path="/api/elite/truck/update", status_code=status.HTTP_200_OK)
    async def update_truck(self, truck_id: str):
        """Updates the data of a particular truck id"""
        pass

    @router.post(path="/api/elite/truck/upload",status_code=status.HTTP_201_CREATED)
    async def upload_truck_excel(self):
        """Upload a excel file with the truck data"""
        pass
