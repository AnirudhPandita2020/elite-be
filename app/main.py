from fastapi import FastAPI

from app.controller import user_controller, truck_controller, certificate_controller

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

app.include_router(user_controller.router)
app.include_router(truck_controller.router)
app.include_router(certificate_controller.router)
