from django.urls import path
from .views import *


urlpatterns = [
    path('login_veh/', login_veh.as_view())
]
