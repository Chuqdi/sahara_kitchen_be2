from .views import GetUserReferals, TransferToPlayWallet
from django.urls import path


urlpatterns =[
    path("get_user_referals/", GetUserReferals.as_view(), name="referals_retrieved"),
]