from fastapi_users import InvalidPasswordException

from app.core import settings


def password_length_validator(password: str):
    if len(password) < settings.password_length:
        raise InvalidPasswordException(
            f'Пароль должен быть длиной не менее '
            f'{settings.password_length} символов.')


def password_content_validator(password: str, email: str):
    if email in password:
        raise InvalidPasswordException(
            'В пароле не должно содержаться e-mail.')
