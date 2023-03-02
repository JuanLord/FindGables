from django.urls import path
from .views import *

urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('index', index),
    path('about', about),
    path('attractions', attractions),
    path('map', map),
    path('itinerary', itinerary),
    path('location/<str:name>', location, name="location"),
    path('functions', functions, name="functions")
]