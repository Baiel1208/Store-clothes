from django.urls import path

from apps.orders import views

urlpatterns = [
    path('order-create/', views.OrderCreateView.as_view(), name='order_create'),

]