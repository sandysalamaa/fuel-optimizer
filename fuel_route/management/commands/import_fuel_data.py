import csv
import decimal
import time

from django.core.management.base import BaseCommand
from fuel_route.models import FuelStation
from fuel_route.services.ors_service import geocode_location


class Command(BaseCommand):
    help = "Import fuel data from CSV and geocode it"

    def handle(self, *args, **kwargs):

        city_cache = {}   #  cache 

        with open("fuel-prices-for-be-assessment.csv", newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                truckstop_name = row["Truckstop Name"]
                address = row["Address"]
                city = row["City"]
                state = row["State"]
                price = decimal.Decimal(row["Retail Price"])

                city_key = f"{city}, {state}"

                try:
                    if city_key in city_cache:
                        longitude, latitude = city_cache[city_key]
                    else:
                        coords = geocode_location(city_key)
                        longitude, latitude = coords
                        city_cache[city_key] = coords
                        time.sleep(1)  # API limit

                    station, created = FuelStation.objects.update_or_create(
                        truckstop_name=truckstop_name,
                        address=address,
                        city=city,
                        state=state,
                        defaults={
                            "price": price,
                            "latitude": latitude,
                            "longitude": longitude,
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created {city_key}"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Updated {city_key}"))

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Failed {city_key}: {str(e)}")
                    )