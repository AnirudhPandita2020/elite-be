from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user_model import User


def save(user: User, db: Session) -> User:
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
    return user


def findByEmail(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).one_or_none()


def findById(user_id: int, db: Session) -> User:
    return db.query(User).filter(User.id == user_id).one_or_none()


def addProfileUrl(url: str, db: Session, user: User):
    db.query(User).filter(User.email == user.email).update({
        User.profile_photo: url
    }, synchronize_session=False)
    db.commit()


def fetchUserList(user: User, db: Session):
    return db.query(User).filter(User.email != user.email).all()


def updateActiveStatus(email: str, is_active: bool, authority_level: int, db: Session, role: str):
    db.query(User).filter(User.email == email).update({
        User.is_active: is_active,
        User.authority_level: authority_level,
        User.role: role
    }, synchronize_session=False)
    db.commit()
