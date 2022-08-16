import django_filters
from django_filters import FilterSet, DateFilter
from .models import *


# Фильтр для модели затяжек
class TighteningFilter(FilterSet):

    class Meta:
        # привязка к моделе
        model = Tightening
        # определение полей для фильтрации
        fields = {
            'nutrunner': ['exact'],  # должно быть полное совпадение с тем, что указал пользователь
            'vin__vin_number': ['icontains'],
            'vin__model': ['exact'],
            'time_of_creation': ['gte'],  # время создания должно быть больше или равно тому, что указал пользователь
            'printing': ['exact'],
        }


# Фильтр для модели овтомобиля
class VehicleFilter(FilterSet):

    class Meta:
        model = Vehicle
        fields = {
            'vin_number': ['icontains'],  # можно ввести только чать символов
            'model': ['exact'],  # должно быть полное совпадение с тем, что указал пользователь
        }
