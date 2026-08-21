from app.repositories.user_repository import find_user_by_credentials
from app.repositories.user_repository import (
    find_user_by_credentials,
    create_user
)


def authenticate_user(username, password):
    return find_user_by_credentials(username, password)


def register_user(username, password):
    create_user(username, password)

def authenticate_user(username, password):
    return find_user_by_credentials(username, password)