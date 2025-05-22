from square.client import Client
from django.conf import settings
import uuid

def get_square_client():
    return Client(
        access_token=settings.SQUARE_ACCESS_TOKEN,
        environment=settings.SQUARE_ENVIRONMENT
    )