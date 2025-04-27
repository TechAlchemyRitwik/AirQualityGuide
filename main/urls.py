from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aqi/', views.aqi_checker, name='aqi'),
    path('aqi-levels/', views.aqi_levels, name='aqi_levels'),
    path('blogs/', views.blogs, name='blogs'),
    path('about/', views.about, name='about'),
    path("chatbot/", views.chatbot, name="chatbot"),

]
