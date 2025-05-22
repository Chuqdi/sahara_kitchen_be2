from .models import Referal
from rest_framework import serializers
from users.serializers import SignUpSerializer



class ReferializerSerilizer(serializers.ModelSerializer):
    refering = SignUpSerializer()

    class Meta:
        model = Referal
        fields =[
             "refered_by",
             "refering",
             "amount",
             "is_deposited",
             "date_created_formatted",
             "refering",
             "recieved"
        ]
        extra_kwargs ={
            "date_created_formatted":{
                "read_only":True
            }
        }