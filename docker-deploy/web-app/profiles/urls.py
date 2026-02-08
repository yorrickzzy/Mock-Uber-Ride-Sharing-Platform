from django.urls import path, include
from . import views as v
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', v.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='profiles/logout.html'), name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('driver/register/', v.register_driver, name='register_driver'),
    path('driver/', v.driver_detail, name='driver_detail'),
    path('driver/edit/', v.edit_driver, name='edit_driver'),
]
