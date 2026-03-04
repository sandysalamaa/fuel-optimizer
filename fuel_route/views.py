
#----------------------------------------------------------------------------
#Here we fetch the route from OpenRouteService and decode the geometry.
#----------------------------------------------------------------------------

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.ors_service import (
    geocode_location,
    get_route,
    validate_within_usa
)
from .services.geometry_service import decode_geometry
from .models import FuelStation
from .services.fuel_service import haversine


@api_view(['POST'])
def route_test(request):
    try:
        start_text = request.data.get("start")
        end_text = request.data.get("end")

        start_coords = geocode_location(start_text)
        end_coords = geocode_location(end_text)

        route_data = get_route(start_coords, end_coords)

        distance_meters = route_data["routes"][0]["summary"]["distance"]
        geometry = route_data["routes"][0]["geometry"]

        distance_miles = distance_meters * 0.000621371

        decoded_geometry = decode_geometry(geometry)

        return Response({
            "distance_miles": round(distance_miles, 2),
            "geometry": decoded_geometry
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['POST'])
def fuel_route(request):
    #----------------------------------------------------------------------------
    # The API geocodes the input cities, fetches the route once, decodes the route geometry, 
    # samples points along the route, finds nearby fuel stations from the database,
    # selects the cheapest option, and calculates the total fuel cost.
    #----------------------------------------------------------------------------

    try:
        start_text = request.data.get("start")
        end_text = request.data.get("end")

        start_coords = geocode_location(start_text)
        end_coords = geocode_location(end_text)

        route_data = get_route(start_coords, end_coords)

        distance_meters = route_data["routes"][0]["summary"]["distance"]
        geometry = route_data["routes"][0]["geometry"]

        distance_miles = distance_meters * 0.000621371

        decoded_points = decode_geometry(geometry)

        route_points = decoded_points[::50]

        stations = FuelStation.objects.all()

        fuel_stops = []

        for lat, lon in route_points:

            nearby = []

            for station in stations:

                dist = haversine(
                    lat,
                    lon,
                    station.latitude,
                    station.longitude
                )

                if dist < 50:
                    nearby.append(station)

            if nearby:
                cheapest = min(nearby, key=lambda x: x.price)

                # fuel_stops.append({
                #     "city": cheapest.city,
                #     "truckstop_name": cheapest.truckstop_name,
                #     "price": float(cheapest.price),
                #     "latitude": cheapest.latitude,
                #     "longitude": cheapest.longitude,
                #     "stops_count": len(fuel_stops)
                # })
                fuel_stops.append({
                    "city": cheapest.city,
                    "truckstop_name": cheapest.truckstop_name,
                    "price": float(cheapest.price),
                    "latitude": cheapest.latitude,
                    "longitude": cheapest.longitude
                })

        stops_needed = int(distance_miles // 500)

        fuel_stops = fuel_stops[:stops_needed]

        mpg = 10
        gallons_needed = distance_miles / mpg

        if fuel_stops:
            avg_price = sum(s["price"] for s in fuel_stops) / len(fuel_stops)
        else:
            avg_price = 0

        total_cost = gallons_needed * avg_price

        # return Response({
        #     "distance_miles": round(distance_miles, 2),
        #     "fuel_stops": fuel_stops,
        #     "total_fuel_cost": round(total_cost, 2)
        # })
        return Response({
            "distance_miles": round(distance_miles, 2),
            "stops_count": stops_needed,
            "fuel_stops": fuel_stops,
            "total_fuel_cost": round(total_cost, 2),
            "route_geometry": decoded_points
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)