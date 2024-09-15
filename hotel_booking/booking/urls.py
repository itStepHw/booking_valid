from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('register/', views.register, name='register'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('rooms/new/', views.room_create, name='room_create'),
    path('bookings/new/', views.booking_create, name='booking_create'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('rooms/<int:pk>/edit/', views.room_update, name='room_update'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),
    path('bookings/<int:pk>/cancel/', views.booking_cancel, name='booking_cancel'),
]