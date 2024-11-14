from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_home, name='service_home'),  # Main service page
    path('online/', views.online_service, name='online_service'),
    path('map/', views.map_service, name='map_service'),
    path('profile/', views.profile_view, name='profile'),
    path('map_detail/', views.map_detail, name='map_detail'),
    path('ask_doctor/', views.ask_doctor, name='ask_doctor'),
]