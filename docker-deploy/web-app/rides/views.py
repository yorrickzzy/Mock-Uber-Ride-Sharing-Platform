from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
from .models import Rides
from .forms import RequestRideForm
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.

class RideList(LoginRequiredMixin, ListView):
    model = Rides
    template_name = 'rides/view_rides.html'
    context_object_name = 'rides'

    def get_queryset(self):
        return (
            Rides.objects
            .select_related('vehicle__driver')
            .filter(
                Q(owner=self.request.user) |
                Q(sharers=self.request.user)
            )
            .distinct()
        )

class UpcomingRideList(LoginRequiredMixin, ListView):
    model = Rides
    template_name = 'rides/view_rides.html'
    context_object_name = 'rides'

    def get_queryset(self):
        return (
            Rides.objects
            .select_related('vehicle__driver')
            .filter(
                Q(owner=self.request.user) |
                Q(sharers=self.request.user),
                is_completed=False
            )
            .distinct()
        )

class CompletedRideList(LoginRequiredMixin, ListView):
    model = Rides
    template_name = 'rides/view_rides.html'
    context_object_name = 'rides'

    def get_queryset(self):
        return (
            Rides.objects
            .select_related('vehicle__driver')
            .filter(
                Q(owner=self.request.user) |
                Q(sharers=self.request.user),
                is_completed=True
            )
            .distinct()
        )

class UpdateRide(LoginRequiredMixin, UpdateView):
    model = Rides
    form_class = RequestRideForm
    template_name = 'rides/ride_form.html'
    success_url = '/rides/view/'
    def get_queryset(self):
        return Rides.objects.filter(owner=self.request.user)

@login_required
def request_ride(request):
    if request.method == 'POST':
        request_ride_form = RequestRideForm(request.POST)
        if request_ride_form.is_valid():
            ride = request_ride_form.save(commit=False)
            ride.owner = request.user
            ride.vehicle = None
            ride.is_confirmed = False
            ride.is_completed = False
            ride.save()
            return redirect('view_rides')
    else:
        request_ride_form = RequestRideForm()
    return render(request, 'rides/ride_form.html', {'form': request_ride_form})

@login_required
def view_ride_details(request, pk):
    ride = get_object_or_404(
        Rides.objects.select_related('vehicle__driver'),
        pk=pk
    )
    is_driver = (
        ride.vehicle is not None
        and hasattr(request.user, "driverprofile")
        and ride.vehicle.driver.user_id == request.user.id
    )
    if (
        ride.owner != request.user
        and request.user not in ride.sharers.all()
        and not is_driver
    ):
        return redirect('view_rides')

    return render(
        request,
        'rides/ride_details.html',
        {
            'ride': ride,
            'is_driver': is_driver,
        }
    )

@login_required
def cancel_ride(request, pk):
    ride = get_object_or_404(Rides, pk=pk, owner=request.user)
    if ride.is_confirmed:
        return redirect('ride_details', pk=pk)
    ride.delete()
    return redirect('view_rides')

@login_required
def leave_ride(request, pk):
    ride = get_object_or_404(Rides, pk=pk)
    if ride.owner == request.user:
        return redirect('ride_details', pk=pk)
    if request.user not in ride.sharers.all():
        return redirect('view_rides')
    if ride.is_confirmed:
        return redirect('ride_details', pk=pk)
    ride.sharers.remove(request.user)
    ride.num_passengers = 1 + ride.sharers.count()
    ride.save()
    return redirect('view_rides')

@login_required
def search_sharable_rides(request):
    rides = Rides.objects.filter(
        is_shared=True,
        is_confirmed=False,
        is_completed=False
    ).exclude(owner=request.user)

    destination = request.GET.get('destination')
    earliest = request.GET.get('earliest')
    latest = request.GET.get('latest')
    party_size = request.GET.get('passengers')

    if destination:
        rides = rides.filter(destination__icontains=destination)

    if earliest:
        rides = rides.filter(requested_time__gte=earliest)

    if latest:
        rides = rides.filter(requested_time__lte=latest)

    if party_size:
        party_size = int(party_size)
        MAX_CAPACITY = 5
        rides = rides.filter(num_passengers__lte=MAX_CAPACITY - party_size)

    return render(request, 'rides/search_rides.html', {'rides': rides})


@login_required
def join_ride(request, pk):
    ride = Rides.objects.get(pk=pk)
    if not ride.is_shared or ride.is_confirmed or ride.is_completed:
        return redirect('search_rides')
    if ride.owner == request.user:
        return redirect('search_rides')
    if request.user in ride.sharers.all():
        return redirect('view_rides')
    ride.sharers.add(request.user)
    ride.num_passengers = 1 + ride.sharers.count()
    ride.save()
    return redirect('view_rides')

@login_required
def driver_search_rides(request):
    if not hasattr(request.user, 'driverprofile'):
        return redirect('register_driver')
    vehicle = request.user.driverprofile.vehicle

    qs = Rides.objects.filter(
        is_confirmed=False,
        is_completed=False,
        vehicle__isnull=True,
        num_passengers__lte=vehicle.capacity
    ).filter(
        Q(vehicle_type__iexact='Any') |
        Q(vehicle_type__iexact=vehicle.vehicle_type) |
        Q(vehicle_type__exact='')
    )
    if vehicle.special_info:
        qs = qs.filter(
            Q(special_request='') |
            Q(special_request__exact=vehicle.special_info)
        )
    else:
        qs = qs.filter(special_request='')

    rides = qs.order_by('requested_time')

    return render(request, 'rides/driver_search.html', {'rides': rides})

@login_required
def confirm_ride(request, pk):
    driver = request.user.driverprofile
    vehicle = driver.vehicle

    ride = get_object_or_404(
        Rides,
        pk=pk,
        is_confirmed=False,
        is_completed=False,
        vehicle__isnull=True,
    )

    if ride.owner == request.user or request.user in ride.sharers.all():
        messages.error(request, "You are not allowed to confirm your own ride.")
        return redirect('driver_search_rides')

    if ride.num_passengers > vehicle.capacity:
        return redirect('driver_search_rides')

    if ride.vehicle_type not in ['', 'Any', vehicle.vehicle_type]:
        return redirect('driver_search_rides')

    if ride.special_request:
        if ride.special_request != vehicle.special_info:
            return redirect('driver_search_rides')


    ride.driver = driver.user
    ride.vehicle = vehicle
    ride.is_confirmed = True
    ride.save()

    recipients = set()

    if ride.owner.email:
        recipients.add(ride.owner.email)

    for sharer in ride.sharers.all():
        if sharer.email:
            recipients.add(sharer.email)

    send_mail(
        subject='Your ride has been confirmed!',
        message=(
            f'Your ride to {ride.destination} at {ride.requested_time} has been confirmed.\n\n'
            f'Driver: {driver.full_name}\n'
            f'Vehicle: {vehicle.vehicle_type} ({vehicle.license_plate})\n'
            f'Passengers: {ride.num_passengers}\n'
        ),
        from_email=None,
        recipient_list=list(recipients),
        fail_silently=True,
    )

    return redirect('driver_search_rides')

@login_required
def driver_confirmed_rides(request):
    if not hasattr(request.user, 'driverprofile'):
        return redirect('register_driver')
    driver = request.user.driverprofile

    rides = Rides.objects.filter(
        is_confirmed=True,
        is_completed=False,
        vehicle__driver=driver
    ).order_by('requested_time')

    return render(
        request,
        'rides/driver_confirmed_rides.html',
        {'rides': rides}
    )

@login_required
def complete_ride(request, pk):
    if not hasattr(request.user, 'driverprofile'):
        return redirect('register_driver')
    driver = request.user.driverprofile
    ride = get_object_or_404(
        Rides,
        pk=pk,
        is_confirmed=True,
        is_completed=False,
        vehicle__driver=driver
    )
    ride.is_completed = True
    ride.save()

    return redirect('driver_confirmed_rides')
