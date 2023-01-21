from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.recent_activity_model import RecentActivity


def save(activity: RecentActivity, db: Session):
    try:
        db.add(activity)
        db.commit()
        db.refresh(activity)
    except IntegrityError:
        db.rollback()


def fetch_five_latest_activity(db: Session):
    return db.query(RecentActivity).order_by(RecentActivity.timestamp.desc()).limit(5).all()
