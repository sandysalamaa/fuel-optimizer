# Fuel Optimizer API

This project is a Django-based API that calculates the optimal fuel stops along a route within the United States based on fuel prices and vehicle range.

The API determines the most cost-effective locations to refuel and estimates the total fuel cost for the trip.

---

## Features

- Accepts a start and end location within the United States
- Calculates the driving route between the two locations
- Determines the number of fuel stops required based on vehicle range
- Selects cost-effective fuel stations along the route
- Calculates the estimated total fuel cost
- Uses local fuel price data for fast responses

---

## Assumptions

- Vehicle maximum range: **500 miles**
- Fuel efficiency: **10 miles per gallon**
- Fuel stations are selected based on proximity to the route and lowest price

---

## Technologies Used

- **Python**
- **Django**
- **Django REST Framework**
- **OpenRouteService API** – routing
- **Nominatim (OpenStreetMap)** – geocoding
- **SQLite** – database
- **Polyline** – decoding route geometry

---

## Project Structure
