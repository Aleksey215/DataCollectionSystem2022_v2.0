from django.contrib import admin

from .models import *


@admin.register(Nutrunner)
class NutrunnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'production_line')
    list_display_links = ('name',)
    ordering = ['id']


@admin.register(ProductionLine)
class ProductionLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'line_name')
    list_display_links = ('line_name',)
    ordering = ['id']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'vin_number', 'model')
    list_display_links = ('vin_number',)
    ordering = ['id']


@admin.register(Tightening)
class TighteningAdmin(admin.ModelAdmin):
    list_display = ('vin', 'nutrunner', 'time_of_creation', 'printing')
    list_display_links = ('vin',)
    ordering = ['-time_of_creation']
