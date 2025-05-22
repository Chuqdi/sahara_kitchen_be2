from addresses.serializers import AddressSerializer
from users.models import  ReferalCode, User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from utils.randomString import GenerateRandomString



def checkUserCodeExist():
    code = GenerateRandomString.randomAlhanumeric(6)
    if ReferalCode.objects.filter(code=code).exists():
        checkUserCodeExist()
    return code


class ReferalCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferalCode
        fields=[
            "code"
        ]




class SignUpSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, min_length =8)
    # referal_code = ReferalCodeSerializer(many=False, read_only=True)
    

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "country",
            "addresses",
            "phone_number",
            "is_active"
        ]
        
    
    
    

    def validate(self, attrs):
        if User.objects.filter(phone_number=attrs.get("email")).exists():
            raise ValidationError("User phone number already taken")


        # if User.objects.filter(phone_number=attrs.get("phone_number")).exists():
        #     raise ValidationError("User phone number already taken")
        
        # if User.objects.filter(username=attrs.get("username")).exists():
        #     raise ValidationError("User with this username already taken")
            
        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        referalCode =checkUserCodeExist()
        r =ReferalCode.objects.create(user=user, code = referalCode)
        user.save()
        Token.objects.create(user=user)
        return user
        
class UserVerfifyAccountSerializer(serializers.Serializer):
    code = serializers.CharField()


class UserPhoneNumberVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()



class ResendUserEmailActivationCodeSerializer(serializers.Serializer):
    email = serializers.CharField()

    
    




class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "email",
            "password",
           
        ]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = User.objects.filter(email=email)
        if not user.exists():
            raise ValidationError("User with this Email does not exist")
        
        user = user[0]
        if not user.check_password(password, user.password):
            raise ValidationError("User password validation has failed")



        return attrs
    



class MessageOnlySerializer(serializers.Serializer):
    message= serializers.CharField()



class ReferalCodeSerializer(serializers.ModelSerializer):
    user = SignUpSerializer(many=False, read_only=True)
    class Meta:
        model = ReferalCode
        fields =[
            "code",
            "user"
        ]
        ref_name ="referal_coder"

class EmailOnlySerializer(serializers.Serializer):
    email = serializers.CharField()