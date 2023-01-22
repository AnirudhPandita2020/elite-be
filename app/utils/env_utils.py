import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    database_hostname: str = os.getenv("DATABASE_HOSTNAME")
    database_port: str = os.getenv("DATABASE_PORT")
    database_password: str = os.getenv("DATABASE_PASSWORD")
    database_name: str = os.getenv("DATABASE_NAME")
    database_username: str = os.getenv("DATABASE_USERNAME")
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes: str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    valid_email_allowed: str = os.getenv("VALID_EMAIL_ALLOWED")
    authority_level: str = os.getenv("AUTHORITY_LEVEL")
    allowed_sites: List[str] = os.getenv("ALLOWED_SITES")
    allowed_action: List[str] = os.getenv("ALLOWED_ACTION")
    email_password: str = os.getenv("EMAIL_PASSWORD")
    sender_email: str = os.getenv("SENDER_EMAIL")
    receiver_email: str = os.getenv("RECEIVER_EMAIL")


setting = Settings()


class Firebase(BaseSettings):
    type: str = os.getenv("TYPE")
    project_id: str = os.getenv("PROJECT_ID")
    private_key_id: str = os.getenv("PRIVATE_KEY_ID")
    private_key: str = os.getenv("PRIVATE_KEY")
    client_email: str = os.getenv("CLIENT_EMAIL")
    client_id: str = os.getenv("CLIENT_ID")
    auth_uri: str = os.getenv("AUTH_URI")
    token_uri: str = os.getenv("TOKEN_URI")
    auth_provider_x509_cert_url: str = os.getenv("AUTH_PROVIDER_X509_CERT_URL")
    client_x509_cert_url: str = os.getenv("CLIENT_X509_CERT_URL")
    storage_bucket: str = os.getenv("STORAGE_BUCKET")


firebase_cred = Firebase()
