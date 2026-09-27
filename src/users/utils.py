from fastapi_users.password import PasswordHelper

password_helper = PasswordHelper()


def hash_password(password: str) -> str:
    return password_helper.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    is_valid, _ = password_helper.verify_and_update(password, hashed_password)
    return is_valid
