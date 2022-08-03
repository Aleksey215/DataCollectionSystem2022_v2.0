import django_filters
from django_filters import FilterSet, DateFilter
from .models import *


class TighteningFilter(FilterSet):
    timme_of_creation = DateFilter

    class Meta:
        model = Tightening
        fields = {
            'nutrunner': ['exact'],  # должно быть полное совпадение с тем, что указал пользователь
            'vin__vin_number': ['exact'],  # можно ввести только чать символов
            'vin__model': ['exact'],  # должно быть полное совпадение с тем, что указал пользователь
            'time_of_creation': ['gte'],  # # время создания должно быть больше или равно тому, что указал пользователь
        }


class VehicleFilter(FilterSet):
    timme_of_creation = DateFilter

    class Meta:
        model = Tightening
        fields = {
            'nutrunner': ['exact'],  # должно быть полное совпадение с тем, что указал пользователь
            'vin__vin_number': ['exact'],  # можно ввести только чать символов
            'vin__model': ['exact'],  # должно быть полное совпадение с тем, что указал пользователь
            'time_of_creation': ['gte'],  # # время создания должно быть больше или равно тому, что указал пользователь
        }
