# booking/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Room, Booking
from .forms import UserRegisterForm, RoomForm, BookingForm
from django.urls import reverse_lazy


def index(request):
    return render(request, 'booking/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('room_list')
    else:
        form = UserRegisterForm()
    return render(request, 'booking/register.html', {'form': form})


@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'booking/room_list.html', {'rooms': rooms})


@login_required
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'booking/room_detail.html', {'room': room})


@login_required
def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'booking/room_form.html', {'form': form})


@login_required
def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            booking.users.add(request.user)
            return redirect('room_list')
    else:
        form = BookingForm()
    return render(request, 'booking/booking_form.html', {'form': form})


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(users=request.user)
    return render(request, 'booking/booking_list.html', {'bookings': bookings})


@login_required
def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_detail', pk=room.pk)
    else:
        form = RoomForm(instance=room)
    return render(request, 'booking/room_form.html', {'form': form})


@login_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('room_list')
    return render(request, 'booking/room_confirm_delete.html', {'room': room})


@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.user in booking.users.all():
        if request.method == 'POST':
            booking.delete()
            return redirect('booking_list')
    else:
        return redirect('booking_list')

    return render(request, 'booking/booking_confirm_cancel.html', {'booking': booking})