from django.shortcuts import render
from rest_framework.views import APIView
from addresses.models import Address
from addresses.serializers import AddressSerializer
from rest_framework import status
from rest_framework.response import Response
from users.serializers import SignUpSerializer
from users.models import User




class DeleteAddress(APIView):
    def delete(self, request, id):
        try:
            address = Address.objects.get(id=id)
        except Address.DoesNotExist:
            return Response(data={
                "message":"Address not found",
            }, status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response(data={
                "user":SignUpSerializer(User.objects.get(id=request.user.id)).data,
                "message":"Address deleted successfully"
            }, status=status.HTTP_201_CREATED) 


class UpdateAddress(APIView):
    def patch(self, request, id):
        try:
            address = Address.objects.get(id=id)
        except Address.DoesNotExist:
            return Response(data={
                "message":"Address not found",
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(instance=address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                "user":SignUpSerializer(User.objects.get(id=request.user.id)).data,
                "message":"Address updated successfully"
            }, status=status.HTTP_201_CREATED) 
        
        return Response(data={
            "message": "Error updating address"
        }, status=status.HTTP_400_BAD_REQUEST)


class AddAddress(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id

        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                "user":SignUpSerializer(User.objects.get(id=request.user.id)).data,
                "message":"Address saved successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(data={
            "message": "Error saving address"
        }, status=status.HTTP_400_BAD_REQUEST)
            