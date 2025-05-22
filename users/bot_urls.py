from django.urls import path
from .bot_views import Me, LoginUserView,LogoutUser


urlpatterns =[
    path("login/", LoginUserView.as_view(), name="login_user"),
    path("me/<telegram_id>/", Me.as_view(), name="check_user"),
    path("logout/<telegram_id>/", LogoutUser.as_view(), name="logout_user"),
]