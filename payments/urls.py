from django.urls import path
from .views import CreatePaymentIntent,create_payment

urlpatterns = [
    path("create_intent/<amount>",CreatePaymentIntent.as_view(), name="create_intent" ),
    path("create_intent_square/",create_payment, ),
    
]
