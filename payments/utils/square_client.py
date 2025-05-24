# from square.client import Client
from square import client
from django.conf import settings
import uuid


def get_square_client():
    return client(
        access_token=settings.SQUARE_ACCESS_TOKEN,
        environment=settings.SQUARE_ENVIRONMENT
    )