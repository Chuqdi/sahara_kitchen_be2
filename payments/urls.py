from django.urls import path
from .views import CreatePaymentIntent, confirm_sumup_payment,create_payment, create_sumup_checkout, create_pay_on_delivery_order

urlpatterns = [
    path("create_intent/<amount>",CreatePaymentIntent.as_view(), name="create_intent" ),
    path("create_intent_square/",create_payment, ),
    path("create_sumup_checkout/", create_sumup_checkout),
    path("confirm_sumup_payment/", confirm_sumup_payment),
    path("create_pay_on_delivery_order/", create_pay_on_delivery_order)
    
]
