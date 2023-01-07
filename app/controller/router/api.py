from fastapi import APIRouter

from app.controller import admin_controller, user_controller, truck_controller, certificate_controller

main_router = APIRouter()

main_router.include_router(admin_controller.router)
main_router.include_router(user_controller.router)
main_router.include_router(truck_controller.router)
main_router.include_router(certificate_controller.router)