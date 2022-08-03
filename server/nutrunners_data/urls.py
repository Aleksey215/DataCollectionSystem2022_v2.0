from django.urls import path

from .views import *


urlpatterns = [
    # адрес к списку всех затяжек
    path('', TighteningList.as_view()),
    # адрес для поиска объектов
    path('search/', TighteningSearch.as_view(), name='search'),
    # отображение затяжек, которые уже отпечатаны
    path('archive/', TighteningArchiveList.as_view(), name='archive'),
    # подробная информация о затяжке
    path('<int:pk>/', TighteningDetail.as_view(), name='tightening_detail'),
    # # попытка создать PDF файл
    # # path('create_a_check/', create_a_check, name='create_a_check'),
    # подробная информация по vin
    path('vin_detail/<int:pk>/', VehicleDetailView.as_view(), name='vin_detail'),
]
