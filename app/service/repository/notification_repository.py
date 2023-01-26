from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.notification_model import Notification


def save(notification_model: Notification, db: Session) -> Notification:
    try:
        db.add(notification_model)
        db.commit()
        db.refresh(notification_model)
        return notification_model
    except IntegrityError:
        db.rollback()


def find_by_email(email: str, db: Session) -> Notification:
    return db.query(Notification).filter(Notification.email_id == email).one_or_none()


def update_token(token: str, email: str, db: Session):
    db.query(Notification).filter(Notification.email_id == email).update({
        Notification.token: token
    }, synchronize_session=False)
    db.commit()


def get_all_token(db: Session) -> List[Notification]:
    return db.query(Notification).all()
