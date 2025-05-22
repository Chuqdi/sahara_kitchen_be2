from django.utils import timezone
from utils.EmailSender import send_activation_email
from utils.randomString import GenerateRandomString
from users.models import  User, UserEmailActivationCode
from datetime import timedelta
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from utils.TokenGenerator import generateToken



def generateUserOTP(e):
    user = User.objects.get(email=e)
    code = GenerateRandomString.randomStringGenerator(6).upper()
    c = UserEmailActivationCode.objects.create(user=user, code =code)
    return code


def generateSecureEmailCredentials(user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = generateToken.make_token(user)

    return {"uidb64": uidb64, "token": token}



def sendUserActivationEmail(email, request):
    user = User.objects.get(email=email)
    secureEmailCredentials = generateSecureEmailCredentials(user)
    token = secureEmailCredentials.get("token")
    uidb64 = secureEmailCredentials.get("uidb64")
    domain = get_current_site(request).domain
    urlPath = f"{domain}/api/v1/users/activate_account/{token}/{uidb64}/"
    send_activation_email(
        user=user,
        request=request,
        template="emails/user_account_activation.html",
        urlPath=urlPath,
        subject="Account Email Activation",
    )


def validateOTPCode(code):
    
        c = UserEmailActivationCode.objects.filter(code = code)

        if not c.exists():
            return {
                "message":"OTP does not exist",
                "type":False
            }

        code = c[0]
        if (code.date_created + timedelta(minutes=30)) < timezone.now():
            code.delete()
            return {
                "message":"OTP has expired",
                "type":False,
            }
        code.delete()

        return  {
                "message":"OTP is valid",
                "type":True,
                "code":code
            }




