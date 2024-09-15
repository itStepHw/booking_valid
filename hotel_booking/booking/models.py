from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('SINGLE', 'Одноместный'),
        ('DOUBLE', 'Двухместный'),
        ('SUITE', 'Люкс'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])#нашел в документации
    description = models.TextField()
    photo = models.ImageField(upload_to='room_photos/')

    def __str__(self):
        return f'{self.room_number} - {self.room_type}'


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    users = models.ManyToManyField(User, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Бронирование {self.room.room_number} от {self.check_in} до {self.check_out}'

