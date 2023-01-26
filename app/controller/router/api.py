from fastapi import APIRouter

from app.controller import user_controller, truck_controller, certificate_controller, notification_controller
from app.exceptions.handler.route_handler import RouteErrorHandler

main_router = APIRouter(route_class=RouteErrorHandler)

main_router.include_router(user_controller.router)
main_router.include_router(truck_controller.router)
main_router.include_router(certificate_controller.router)
main_router.include_router(notification_controller.router)


@main_router.get("/")
async def health_check():
    return {'status': 'ok'}
