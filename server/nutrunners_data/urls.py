"""
файл с адресами для перехода на соответствующие страницы приложения
"""
from django.urls import path
# импортируем все представления
from .views import *


# указываем адреса для каждого представления
urlpatterns = [
    # адрес для поиска объектов
    path('search/', TighteningSearch.as_view(), name='search_tightenings'),
    # попытка создать PDF файл
    path('vin_detail/<int:pk>/print_a_check/', print_check_manually, name='print_check_manually'),
    # подробная информация по vin
    path('vin_detail/<int:pk>/', VehicleDetailView.as_view(), name='vin_detail'),
    # список винов
    path('', VehicleSearch.as_view(), name='list_of_vins'),
]
