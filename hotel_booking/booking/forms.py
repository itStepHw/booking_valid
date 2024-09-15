from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from datetime import date

from .models import Room, Booking


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price_per_night', 'description', 'photo']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['check_in'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['check_out'].widget = forms.DateInput(attrs={'type': 'date'})

    def clean_check_in(self):
        check_in = self.cleaned_data.get('check_in')
        if check_in is None:
            raise ValidationError("Дата заезда должна быть указана.")
        if check_in < date.today():
            raise ValidationError("Дата заезда не может быть в прошлом.")
        return check_in

    def clean_check_out(self):
        check_in = self.cleaned_data.get('check_in')
        check_out = self.cleaned_data.get('check_out')

        if check_in is None or check_out is None:
            raise ValidationError("Обе даты, заезда и выезда, должны быть указаны.")

        if check_out <= check_in:
            raise ValidationError("Дата выезда должна быть позже даты заезда.")
        return check_out
