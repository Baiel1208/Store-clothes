from django.urls import path
from django.contrib.auth.decorators import login_required


from apps.users import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', login_required(views.UserProfileView.as_view()), name='profile'),
    path('logout/', views.logout, name='logout'),

]