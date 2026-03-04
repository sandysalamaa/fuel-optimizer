from .views import route_test, fuel_route
from django.urls import path

urlpatterns = [
    path('route/', route_test, name='route_test'),
    path('fuel-route/', fuel_route, name='fuel_route'),

]
