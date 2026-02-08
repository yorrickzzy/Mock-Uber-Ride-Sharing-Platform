from django.urls import path
from . import views as v

urlpatterns = [
    path('view/', v.RideList.as_view(), name='view_rides'),
    path('request/', v.request_ride, name='request_ride'),
    path('details/<int:pk>/', v.view_ride_details, name='ride_details'),
    path('cancel/<int:pk>/', v.cancel_ride, name='cancel_ride'),
    path('leave/<int:pk>/', v.leave_ride, name='leave_ride'),
    path('update/<int:pk>/', v.UpdateRide.as_view(), name='update_ride'),
    path('view/upcoming/', v.UpcomingRideList.as_view(), name='upcoming_rides'),
    path('view/completed/', v.CompletedRideList.as_view(), name='completed_rides'),
    path('search/', v.search_sharable_rides, name='search_rides'),
    path('join/<int:pk>/', v.join_ride, name='join_ride'),
    path('driver/search/', v.driver_search_rides, name='driver_search_rides'),
    path('rides/confirm/<int:pk>/', v.confirm_ride, name='confirm_ride'),
    path('driver/confirmed/', v.driver_confirmed_rides, name='driver_confirmed_rides'),
    path('driver/complete/<int:pk>/', v.complete_ride, name='complete_ride'),
]
