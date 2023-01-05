import re

from app.utils.env_utils import setting


def check_valid_company_email(email: str) -> bool:
    email_pattern = r'^[a-zA-Z0-9-_]+@' + setting.valid_email_allowed
    return True if re.match(email_pattern, email) else False
