from firebase_admin import messaging

from app.models.user_model import User
from app.service.repository.notification_repository import *


async def save_token(token: str, user: User, db: Session):
    old_token = find_by_email(user.email, db)
    if old_token:
        update_token(token, user.email, db)
        return {'message': 'Token Updated'}
    else:
        new_notification_model = Notification()
        new_notification_model.email_id = user.email
        new_notification_model.token = token
        save(new_notification_model, db)
        return {'message': 'Token Saved'}


async def send_notification(db: Session, truck_count: int):
    token = [codes.token for codes in get_all_token(db)]
    if truck_count != 0:
        data = {
            'type': 'REMIND',
            'title': 'Attention Elite User!!',
            'message': f'Certificates of about {truck_count} trucks is gonna expire soon.Tap here to more'
        }
        message = messaging.MulticastMessage(
            tokens=token,
            data=data
        )

        response = messaging.send_multicast(message)
        return {'status': 'Delivered'} if response.failure_count == 0 else {'status': 'Failed to deliver to all host'}
