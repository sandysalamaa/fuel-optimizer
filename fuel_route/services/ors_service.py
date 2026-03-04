#----------------------------------------------------------------------------
# Handles geocoding and routing using OpenRouteService.
#----------------------------------------------------------------------------

import requests
from django.conf import settings


GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"
DIRECTIONS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

import requests

def geocode_location(location):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": location,
        "format": "json",
        "limit": 1,
        "countrycodes": "us"
    }

    headers = {
        "User-Agent": "fuel-optimizer-app"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Geocoding Error: {response.text}")

    data = response.json()

    if not data:
        raise Exception("Location not found")

    latitude = float(data[0]["lat"])
    longitude = float(data[0]["lon"])

    return [longitude, latitude]


def get_route(start_coords, end_coords):
    headers = {
        "Authorization": settings.ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            start_coords,
            end_coords
        ]
    }

    response = requests.post(DIRECTIONS_URL, json=body, headers=headers)


    if response.status_code != 200:
        raise Exception(f"Directions Error: {response.text}")

    return response.json()


def validate_within_usa(coords):
    lon, lat = coords

    # Approx US bounding box
    if not (-125 <= lon <= -66 and 24 <= lat <= 49):
        raise Exception("Location must be within USA")