from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Car, Rental
from .forms import RentalForm, RegisterForm, CarForm


def car_list(request):
    cars = Car.objects.filter(available=True)
    return render(request, 'myapp/index.html', {'cars': cars})


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    form = RentalForm()
    return render(request, 'myapp/detail.html', {'car': car, 'form': form})


@login_required
def rent_car(request, pk):
    car = get_object_or_404(Car, pk=pk, available=True)
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.car = car
            rental.user = request.user
            rental.save()
            return redirect('myapp:rental_success', rental_id=rental.id)
    return redirect('myapp:car_detail', pk=pk)


def rental_success(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    return render(request, 'myapp/success.html', {'rental': rental})


@login_required
def dashboard(request):
    rentals = Rental.objects.filter(user=request.user).select_related('car')
    return render(request, 'myapp/dashboard.html', {'rentals': rentals})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('myapp:car_list')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('myapp:car_list')


# Password Reset Views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'myapp/password_reset.html'
    email_template_name = 'myapp/password_reset_email.html'
    subject_template_name = 'myapp/password_reset_subject.txt'
    success_url = reverse_lazy('myapp:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'myapp/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'myapp/password_reset_confirm.html'
    success_url = reverse_lazy('myapp:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'myapp/password_reset_complete.html'


# Admin Dashboard Views
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('myapp:car_list')
    
    stats = {
        'total_cars': Car.objects.count(),
        'available_cars': Car.objects.filter(available=True).count(),
        'total_rentals': Rental.objects.count(),
        'active_rentals': Rental.objects.filter(
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date()
        ).count(),
        'total_users': User.objects.count(),
        'recent_rentals': Rental.objects.select_related('car', 'user').order_by('-created_at')[:10],
    }
    return render(request, 'myapp/admin/dashboard.html', stats)


@login_required
def admin_cars(request):
    if not request.user.is_staff:
        return redirect('myapp:car_list')
    cars = Car.objects.all().order_by('-created_at')
    return render(request, 'myapp/admin/cars.html', {'cars': cars})


@login_required
def admin_car_add(request):
    if not request.user.is_staff:
        return redirect('myapp:car_list')
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myapp:admin_cars')
    else:
        form = CarForm()
    return render(request, 'myapp/admin/car_form.html', {'form': form, 'title': 'Add Car'})


@login_required
def admin_car_edit(request, pk):
    if not request.user.is_staff:
        return redirect('myapp:car_list')
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('myapp:admin_cars')
    else:
        form = CarForm(instance=car)
    return render(request, 'myapp/admin/car_form.html', {'form': form, 'title': 'Edit Car', 'car': car})


@login_required
def admin_car_delete(request, pk):
    if not request.user.is_staff:
        return redirect('myapp:car_list')
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('myapp:admin_cars')
    return render(request, 'myapp/admin/car_confirm_delete.html', {'car': car})


@login_required
def admin_rentals(request):
    if not request.user.is_staff:
        return redirect('myapp:car_list')
    rentals = Rental.objects.select_related('car', 'user').order_by('-created_at')
    return render(request, 'myapp/admin/rentals.html', {'rentals': rentals})


@login_required
def admin_users(request):
    if not request.user.is_staff:
        return redirect('myapp:car_list')
    users = User.objects.annotate(rental_count=Count('rentals')).order_by('-date_joined')
    return render(request, 'myapp/admin/users.html', {'users': users})