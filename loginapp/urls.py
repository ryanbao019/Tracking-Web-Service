from django.urls import path
from . import views
from .views import register_view, login_view
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', views.home, name='home'),  # Root URL mapped to the home view
    path('register/', register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-email/', views.verify_email, name='verify_email'),


]

