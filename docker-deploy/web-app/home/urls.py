from django.urls import path, include
from . import views as v

urlpatterns = [
    path('', v.home, name="home"),
    path('rides/', include('rides.urls')),
]