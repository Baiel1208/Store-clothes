from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from apps.product import views

urlpatterns = [
    path('', views.products, name='products'),
    path('basket/add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),

]