
from django.urls import path, include
from .views import ActivateUserEmail, ChangePassword, CheckUserPassword, ContinueForgotPassword, DeleteUserAccount,  ForgotPasswordRequest, GetAllUsers, GetUserReferalCode, RegisterUserView, LoginUserView, ResendUserEmailActivationCode, SendUserMessage, UpdateUserProfile,  UserMe, LogoutUser,UserMeAuth, VerifyUserOTP,GetDashboardDetails, Contact



urlpatterns = [
    path("send_message/", Contact.as_view(), name="send_message"),
    path("send_user_message", SendUserMessage.as_view(), name="send_message"),
    path("get_dashboard_details",GetDashboardDetails.as_view(), name="get_dashboard_details"),
    path("get_all_users/", GetAllUsers.as_view(), name="get_all_users"),
    path("register", RegisterUserView.as_view(), name="register_user"),
    path("login", LoginUserView.as_view(), name="login_user"),
    path("logout", LogoutUser.as_view(), name="logout"),
    path("me/", UserMeAuth.as_view(), name="user_me_auth"),
    path("get_user_referal_code/", GetUserReferalCode.as_view(), name="get_user_referal_code"),
    path("resend_user_account_activation_email/", ResendUserEmailActivationCode.as_view(), name="resend_user_account_activation_email/"),
    path("forgot_password/", ForgotPasswordRequest.as_view(), name="forgot_password"),
    path("continue_forgot_password/", ContinueForgotPassword.as_view(), name="continue_forgot_password"),
    path("activate_account/<token>/<uidb64>/",  ActivateUserEmail.as_view(), name="activateUserAccount"),
    path("verify_user_account_otp/", VerifyUserOTP.as_view(), name="verify_user_account_otp"),
    path("check_user_password/",CheckUserPassword.as_view(), name="check_user_password"),
    path("delete_account/", DeleteUserAccount.as_view(), name="delete_account"),
    path("change_password/", ChangePassword.as_view(), name="change_password"),
    path("update_user_profile", UpdateUserProfile.as_view(), name="update_user_profile"),
    path("me/<int:id>/", UserMe.as_view(), name="user_me"),

    
]