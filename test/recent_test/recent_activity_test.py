from typing import List

from app.models.recent_activity_model import RecentActivity
from test.truck_test.truck_test import test_add_new_truck_with_authority
from test.user_test.user_test import test_elite_user_strong_password


def test_truck_add_recent_activity(client_app, local_database_session):
    test_add_new_truck_with_authority(client_app, local_database_session)
    recent_truck_activity: List[RecentActivity] = local_database_session.query(RecentActivity).order_by(
        RecentActivity.timestamp.desc()).limit(1).all()

    assert recent_truck_activity[0].activity_type == "ADD"


def test_user_add_recent_activity(client_app, local_database_session):
    test_elite_user_strong_password(client_app)
    recent_truck_activity: List[RecentActivity] = local_database_session.query(RecentActivity).order_by(
        RecentActivity.timestamp.desc()).limit(1).all()

    assert recent_truck_activity[0].activity_type == "ADD"
