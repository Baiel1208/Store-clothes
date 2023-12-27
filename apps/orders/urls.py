from django.urls import path

from apps.orders import views

urlpatterns = [
    path('order-create/', views.OrderCreateView.as_view(), name='order_create'),
    path('order-success/', views.SuccessTemplateView.as_view(), name='order_success'),
    path('order-cancel/', views.CanceledTemplateView.as_view(), name='order_cancel'),

]