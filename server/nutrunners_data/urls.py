from django.urls import path

from .views import *


urlpatterns = [
    # адрес к списку всех затяжек
    path('tightenings/', TighteningList.as_view(), name='active_tightenings'),
    # адрес для поиска объектов
    path('search/', TighteningSearch.as_view(), name='search_tightenings'),
    # отображение затяжек, которые уже отпечатаны
    path('archive/', TighteningArchiveList.as_view(), name='archive'),
    # подробная информация о затяжке
    path('<int:pk>/', TighteningDetail.as_view(), name='tightening_detail'),
    # попытка создать PDF файл
    path('vin_detail/<int:pk>/print_a_check/', print_check_manually, name='print_check_manually'),
    # подробная информация по vin
    path('vin_detail/<int:pk>/', VehicleDetailView.as_view(), name='vin_detail'),
    # список винов
    path('', VehicleSearch.as_view(), name='list_of_vins'),
]
