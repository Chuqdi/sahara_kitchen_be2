from django.urls import path

from orders.views import GetAllOrders, GetOrderWithID, MarkAsDelivery




urlpatterns = [
    path("get_all_orders", GetAllOrders.as_view(), name="all_orders"),
    path("mark-as-delivered/<id>", MarkAsDelivery.as_view(), name="mark_as_delivered"),
    path("get_order_with_id/<id>", GetOrderWithID.as_view(), name="get_order_with_id"),
]
