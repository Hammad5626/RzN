from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-player/', views.add_player, name='add_player'),
    path('players/', views.players, name='players'),
    path('players/<int:pk>/edit/', views.edit_player, name='edit_player'),
    path('players/<int:pk>/delete/', views.delete_player, name='delete_player'),
    path('api/timezones/<int:country_id>/', views.country_timezones, name='country_timezones'),
]