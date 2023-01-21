import os
import sys
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.controller.router import api
from app.database.database_engine import get_db
from app.models.certificate_model import Base as certificate_base
from app.models.recent_activity_model import Base as recent_base
from app.models.truck_model import Base as truck_base
from app.models.user_model import Base as user_base

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def start_application() -> FastAPI:
    app = FastAPI()
    app.include_router(api.main_router)
    return app


DATABASE_URL = "postgresql://postgres:Kuld1972poon@localhost:5432/testing"
engine = create_engine(DATABASE_URL)

session_testing = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    user_base.metadata.create_all(bind=engine)
    truck_base.metadata.create_all(bind=engine)
    certificate_base.metadata.create_all(bind=engine)
    recent_base.metadata.create_all(bind=engine)
    _app = start_application()
    yield _app


@pytest.fixture(scope="function")
def local_database_session(app: FastAPI) -> Generator[session_testing, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = session_testing(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client_app(
        app: FastAPI, local_database_session: session_testing
) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        try:
            yield local_database_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
