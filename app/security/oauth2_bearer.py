from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database.database_engine import get_db
from app.exceptions.user_exceptions import UserCredentialException
from app.models.user_model import User
from app.utils.env_utils import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/elite/login")
SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE = setting.access_token_expire_minutes


def create_bearer_token(data: dict) -> str:
    data_to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    data_to_encode.update({"exp": expire})
    return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_bearer_token(token: str):
    try:
        decoded_claim = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded_claim.get("user_id")
        if id is None:
            raise UserCredentialException()
    except JWTError:
        raise UserCredentialException()
    return user_id


def get_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    return db.query(User).filter(User.id == verify_bearer_token(token)).first()
