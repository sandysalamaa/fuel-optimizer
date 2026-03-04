from re import A
from django.contrib import admin


from .models import FuelStation
# admin.site.register(FuelStation)
# @admin.register(FuelStation)
# class FuelStationAdmin(admin.StackedInline):
#     list_display = ('truckstop_name', 'address', 'city', 'state', 'price', 'latitude', 'longitude')



@admin.register(FuelStation)
class FuelStationAdmin(admin.ModelAdmin):
    list_display = (
        "truckstop_name",
        "city",
        "state",
        "price",
    )

    list_filter = (
        "state",
    )

    search_fields = (
        "truckstop_name",
        "city",
        "state",
    )

    ordering = ("price",)
