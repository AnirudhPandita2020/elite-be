import firebase_admin
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from firebase_admin import credentials

from app.controller.router.api import main_router
from app.database.database_engine import sessionLocal
from app.jobs.expire_certificate import check_expire_certificate_of_trucks
from app.utils.env_utils import firebase_cred

app = FastAPI(
    title="Elite Vehicle Certificate Manager",
    description="Backend service for Elite shipping company",
    version="1.0.0",
    contact={
        "name": "Anirudh Pandita",
        "url": "https://www.linkedin.com/in/anirudh-pandita-a0b532200/",
        "email": "kppkanu@gmail.com"
    }
)

app.include_router(main_router)


@app.on_event("startup")
async def start_firebase():
    firebase_admin.initialize_app(
        credentials.Certificate(firebase_cred.dict()), {
            'storageBucket': firebase_cred.storage_bucket
        }
    )


@app.on_event("startup")
@repeat_every(seconds=24 * 60 * 60)
async def elite_background_jobs():
    """Task to be executed every 24 hours"""
    with sessionLocal() as db:
        print(await check_expire_certificate_of_trucks(db=db))
