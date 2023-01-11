import firebase_admin
from fastapi import FastAPI
from firebase_admin import credentials

from app.controller.router.api import main_router
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
