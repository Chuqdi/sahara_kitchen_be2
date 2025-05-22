import threading
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import stripe
from meals.models import Meal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .utils.square_client import get_square_client
import uuid
from django.conf import settings
from orders.models import Order, OrderQuantity
from utils.EmailSender import actionNotificationEmail





class CreatePaymentIntent(APIView):
    permission_classes = [ AllowAny ]
    def post(self, request,amount, *args, **kwargs):
        delivery_first_name = request.data.get("delivery_first_name")
        delivery_last_name = request.data.get("delivery_last_name")
        delivery_phone_number = request.data.get("delivery_phone_number")
        email = request.data.get("email")
        delivery_country = request.data.get("delivery_country")
        items = request.data.get("items")
        is_pay_on_delivery = request.data.get("is_pay_on_delivery")
        delivery_address = request.data.get("delivery_address")



        order = Order()
        

        order.delivery_country = delivery_country
        order.delivery_first_name = delivery_first_name
        order.delivery_last_name = delivery_last_name
        order.delivery_phone_number = delivery_phone_number
        order.email = email
        order.is_pay_on_delivery = is_pay_on_delivery
        order.delivery_address = delivery_address
        if order.delivery_phone_number:
            order.is_paid = False
        order.save()



        
        for item in items:
            try:
                food = Meal.objects.get(id=item.get("food").get("id"))
                quantity = item.get("quantity")
                q = OrderQuantity.objects.create(food = food, quantity = quantity)
                order.quantities.add(q)
            except:
                pass
        
        order.save()

        message_to_customer = f"""
        Your order was received successfully. Be patient as we will reach out to you soon. 
        Sahara Kitchen.
        """
       
        t = threading.Thread(target=actionNotificationEmail, kwargs={
            "name":f"{order.delivery_first_name} {order.delivery_last_name}",
            "to":order.email,
            "message":message_to_customer
        })
        t.start()

        

        
        
        if not order.is_pay_on_delivery:
            stripe.api_key = "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"
            paymentIntent = stripe.PaymentIntent.create(
            amount=int(amount) * 100,
            currency="gbp",
            automatic_payment_methods={"enabled": True},
            )
            message = f"""
            An order was made now. The link below can be used to view details.
            \n
            https://saharakitchenadmin.co.uk/orders/{order.id}
            """
            ##johnson@saharakitchen.co.uk
            t = threading.Thread(target=actionNotificationEmail, kwargs={"name":"Admin", "to":"johnson_onwu@yahoo.co.uk", "message":message})
            t.start()
            return Response(data={
                "paymentIntent":paymentIntent,
                "order_id":order.id,
            }, status=status.HTTP_200_OK)
        else:
            message = f"""
            An order was made now. The link below can be used to view details.
            \n
            https://saharakitchenadmin.co.uk/orders/{order.id}
            """
            ##johnson@saharakitchen.co.uk
            t = threading.Thread(target=actionNotificationEmail, kwargs={"name":"Admin", "to":"johnson_onwu@yahoo.co.uk", "message":message})
            t.start()
            return Response(data={
                "order_id":order.id,
            }, status=status.HTTP_200_OK)





@csrf_exempt
@require_POST
def create_payment(request):
    try:
        data = json.loads(request.body)
        source_id = data.get('sourceId')
        amount = data.get('amount')
        currency = data.get('currency', 'GBP')
        
        
        
        if not source_id or not amount:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
        
        # Initialize Square client
        client = get_square_client()
        
        # Create payment request
        result = client.payments.create_payment(
            body={
                "source_id": source_id,
                "amount_money": {
                    "amount": int(float(amount) * 100),  # Convert to cents
                    "currency": currency
                },
                "location_id": settings.SQUARE_LOCATION_ID,
                "idempotency_key": str(uuid.uuid4())
            }
        )
        
        if result.is_success():
            payment = result.body.get('payment', {})
            delivery_first_name = data.get("delivery_first_name")
            delivery_last_name = data.get("delivery_last_name")
            delivery_phone_number = data.get("delivery_phone_number")
            email = data.get("email")
            delivery_country = data.get("delivery_country")
            items = data.get("items")
            is_pay_on_delivery = data.get("is_pay_on_delivery")
            delivery_address = data.get("delivery_address")



            order = Order()
            

            order.delivery_country = delivery_country
            order.delivery_first_name = delivery_first_name
            order.delivery_last_name = delivery_last_name
            order.delivery_phone_number = delivery_phone_number
            order.email = email
            order.is_pay_on_delivery = is_pay_on_delivery
            order.delivery_address = delivery_address
            order.is_paid = True
            order.save()



            
            for item in items:
                try:
                    food = Meal.objects.get(id=item.get("food").get("id"))
                    quantity = item.get("quantity")
                    q = OrderQuantity.objects.create(food = food, quantity = quantity)
                    order.quantities.add(q)
                except:
                    pass
            
            order.save()

            message_to_customer = f"""
            Your order was received successfully. Be patient as we will reach out to you soon. 
            Sahara Kitchen.
            """
        
            t = threading.Thread(target=actionNotificationEmail, kwargs={
                "name":f"{order.delivery_first_name} {order.delivery_last_name}",
                "to":order.email,
                "message":message_to_customer
            })
            t.start()
            
            
            
            message = f"""
            An order was made now. The link below can be used to view details.
            \n
            https://saharakitchenadmin.co.uk/orders/{order.id}
            """
            ##johnson@saharakitchen.co.uk
            t = threading.Thread(target=actionNotificationEmail, kwargs={"name":"Admin", "to":"johnson_onwu@yahoo.co.uk", "message":message})
            t.start()

            return JsonResponse({
                'success': True,
                'payment_id': payment.get('id'),
                'status': payment.get('status'),
                "order_id":order.id,
                'amount': float(payment.get('amount_money', {}).get('amount', 0)) / 100,
                'currency': payment.get('amount_money', {}).get('currency')
            })
        else:
            return JsonResponse({
                'error': result.errors[0].get('detail', 'Payment processing failed')
            }, status=400)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
