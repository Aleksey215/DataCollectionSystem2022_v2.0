import django_filters
from django_filters import FilterSet, DateFilter
from .models import *


# Фильтр для модели затяжек
class TighteningFilter(FilterSet):
    vin_number = django_filters.CharFilter(
        field_name='vin__vin_number',
        label='VIN автомобиля',
        lookup_expr='icontains'
    )
    model = django_filters.CharFilter(
        field_name='vin__model',
        label='Модель автомобиля',
        lookup_expr='exact'
    )
    time_of_creation = django_filters.DateTimeFilter(
        field_name='time_of_creation',
        label='Дата/Время затяжки',
        lookup_expr='gte',
        input_formats=['%d.%m.%Y', '%d.%m.%Y %H:%M']
    )
    nutrunner = django_filters.ModelChoiceFilter(
        field_name='nutrunner',
        label='Гайковерт',
        lookup_expr='exact',
        queryset=Nutrunner.objects.all()
    )
    printing = django_filters.BooleanFilter(
        field_name='printing',
        label='Статус печати результата',
        lookup_expr='exact'
    )


# Фильтр для модели овтомобиля
class VehicleFilter(FilterSet):
    vin_number = django_filters.CharFilter(
        field_name='vin_number',
        label='VIN автомобиля',
        lookup_expr='icontains'
    )
    model = django_filters.CharFilter(
        field_name='model',
        label='Модель автомобиля',
        lookup_expr='exact'
    )
    check_printed = django_filters.BooleanFilter(
        field_name='check_printed',
        label='Статус чека',
        lookup_expr='exact'
    )
