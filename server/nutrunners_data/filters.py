"""
Файл создан для реализации фильтров, которые будут использоваться в шаблонах
"""

# импорт приложения для создания фильтров
import django_filters
# импорт всех моделей
from .models import *


# фильтр для модели затяжек (наследуемся от класса из приложения)
class TighteningFilter(django_filters.FilterSet):
    # создание поля для фильтрации по вину
    # выведутся все объекты, в которых есть символы, введенные в поле
    vin_number = django_filters.CharFilter(
        field_name='vin__vin_number',
        label='VIN автомобиля',
        lookup_expr='icontains'
    )
    # создание поля для фильтрации по модели
    # выведутся все объекты, которые полностью совпадают с тем, что ввели в поле
    model = django_filters.CharFilter(
        field_name='vin__model',
        label='Модель автомобиля',
        lookup_expr='exact'
    )
    # создание поля для фильтрации по дате и времени
    # выведутся объекты, дата и вемя которых больше чем те, что ввели в поле
    time_of_creation = django_filters.DateTimeFilter(
        field_name='time_of_creation',
        label='Дата/Время затяжки',
        lookup_expr='gte',
        input_formats=['%d.%m.%Y', '%d.%m.%Y %H:%M']  # задаем формат даты и времени для ввода
    )
    # создание поля для фильтрации по имени гайковертов
    # нужно выбрать имя из открывающегося списка
    nutrunner = django_filters.ModelChoiceFilter(
        field_name='nutrunner',
        label='Гайковерт',
        lookup_expr='exact',
        queryset=Nutrunner.objects.all()
    )
    # создание поля для фильтрации по статусу печати результатов затяжки
    # выберается статус из списка
    printing = django_filters.BooleanFilter(
        field_name='printing',
        label='Статус печати результата',
        lookup_expr='exact'
    )


# Фильтр для модели овтомобиля (наследуемся от класса из приложения)
class VehicleFilter(django_filters.FilterSet):
    # создание поля для фильтрации по вину
    # выведутся все объекты, в которых есть символы, введенные в поле
    vin_number = django_filters.CharFilter(
        field_name='vin_number',
        label='VIN автомобиля',
        lookup_expr='icontains'
    )
    # создание поля для фильтрации по модели
    # выведутся все объекты, которые полностью совпадают с тем, что ввели в поле
    model = django_filters.CharFilter(
        field_name='model',
        label='Модель автомобиля',
        lookup_expr='exact'
    )
    # создание поля для фильтрации по статусу печати чека со всеми затяжками
    # выберается статус из списка
    check_printed = django_filters.BooleanFilter(
        field_name='check_printed',
        label='Статус чека',
        lookup_expr='exact'
    )
