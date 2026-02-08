from django.shortcuts import render, redirect
from .forms import RegisterForm, DriverProfileForm, VehicleForm
from django.contrib.auth.forms import AuthenticationForm
from .models import DriverProfile, Vehicle
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'profiles/register.html', {"form": form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
    else:
        form = AuthenticationForm()
    
    return render(request, 'profiles/login.html', {"form": form})

@login_required
def register_driver(request):
    if hasattr(request.user, 'driverprofile'):
        return redirect('driver_detail')

    if request.method == 'POST':
        driver_form = DriverProfileForm(request.POST)
        vehicle_form = VehicleForm(request.POST)

        if driver_form.is_valid() and vehicle_form.is_valid():
            driver = driver_form.save(commit=False)
            driver.user = request.user
            driver.save()

            vehicle = vehicle_form.save(commit=False)
            vehicle.driver = driver
            vehicle.save()

            return redirect('driver_detail')
    else:
        driver_form = DriverProfileForm()
        vehicle_form = VehicleForm()

    return render(request, 'profiles/register_driver.html', {
        'driver_form': driver_form,
        'vehicle_form': vehicle_form,
    })

@login_required
def driver_detail(request):
    driver = request.user.driverprofile
    vehicle = driver.vehicle

    return render(request, 'profiles/driver_detail.html', {
        'driver': driver,
        'vehicle': vehicle,
    })

@login_required
def edit_driver(request):
    driver = request.user.driverprofile
    vehicle = driver.vehicle

    if request.method == 'POST':
        driver_form = DriverProfileForm(request.POST, instance=driver)
        vehicle_form = VehicleForm(request.POST, instance=vehicle)

        if driver_form.is_valid() and vehicle_form.is_valid():
            driver_form.save()
            vehicle_form.save()
            return redirect('driver_detail')
    else:
        driver_form = DriverProfileForm(instance=driver)
        vehicle_form = VehicleForm(instance=vehicle)

    return render(request, 'profiles/edit_driver.html', {
        'driver_form': driver_form,
        'vehicle_form': vehicle_form,
    })
