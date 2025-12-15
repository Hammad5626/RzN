from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-player/', views.add_player, name='add_player'),
    path('api/timezones/<int:country_id>/', views.country_timezones, name='country_timezones'),
]