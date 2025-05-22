import threading
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from orders.models import Order
from rest_framework.permissions import AllowAny
from orders.serializers import OrderSerializer
from utils.EmailSender import actionNotificationEmail



class MarkAsDelivery(APIView):
    def delete(self, request, id):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response(data={
                "message":"Order not found",
            }, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(data={
            "message":"Order has been deleted successfully",
        }, status=status.HTTP_200_OK)
    def patch(self, request, id):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response(data={
                "message":"Order not found",
            }, status=status.HTTP_404_NOT_FOUND)
        order.is_delivered = True
        order.save()
        t = threading.Thread(target=actionNotificationEmail, args=(f"{order.delivery_first_name} {order.delivery_last_name}", order.email, """Your order has been marked as recieved. If you did not receive this order, please contact our customer support."""))
        t.start()
        return Response(data={
            "message":"Order marked as delivered successfully",
        }, status=status.HTTP_200_OK)

class GetAllOrders(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(data={
            "data":{"data":serializer.data}
        }, status=status.HTTP_200_OK)



class GetOrderWithID(APIView):
    permission_classes=[AllowAny]
    def get(self, request,id):
        try:
            order = Order.objects.get(id=id)
            order.save()
        except Order.DoesNotExist:
            return Response(data={
                "message":"Order not found",
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        
        

        return Response(data={
                "data":serializer.data,
            }, status=status.HTTP_200_OK)
        