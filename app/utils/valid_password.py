import re


def check_strong_password(password: str) -> bool:
    strong_password_re = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    return True if re.match(strong_password_re, password) else False
