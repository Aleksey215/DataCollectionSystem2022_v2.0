"""
Файл для реализации представлений
они обрабатывают данные, полученные из моделей и
обработанные бизнес-логикой для отображения в шаблонах (на страницах)
"""
# импорт иодуля для создания фоновых задач
import threading

from django.core.cache import cache
from django.shortcuts import render, redirect
# импортируем дженерики
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView


# Импорт моделей
from .models import *
# Импорт собственных фильтров
from .filters import TighteningFilter, VehicleFilter
# Импорт функции для печати данных
from .services import print_data_from_nutrunners, _create_a_check, \
    _send_file_to_printer, timeout_print_data_from_nutrunners


# Представление для отображения подробной ин-ии об автомобиле
class VehicleDetailView(DetailView):
    # указываем файл шаблона
    template_name = 'nutrunners_data/vin_detail.html'
    # получаем все объекты "автомобиль"
    queryset = Vehicle.objects.all()
    # указываем имя контекста для работы в шаблоне
    context_object_name = 'vehicle'

    def get_object(self, *args, **kwargs):
        """
        Метод для получения объекта
        :param args:
        :param kwargs:
        :return:
        """
        # берем объект из кэша по указанному pk
        obj = cache.get(f'vehicle-{self.kwargs["pk"]}', None)

        # если нет объекта:
        if not obj:
            # создаем его
            obj = super().get_object(*args, **kwargs)
            cache.set(f'vehicle-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        добавляем данные в контекст
        :param object_list:
        :param kwargs:
        :return:
        """
        # получаем контекст
        context = super().get_context_data(**kwargs)
        # добавляем данные в контекст (все затяжки для указанного вина)
        context['tightenings_list'] = Tightening.objects.filter(vin=self.kwargs["pk"])
        # возвращаем контекст
        return context


class TighteningSearch(FilterView):
    """
    Класс для отображения всех затяжек с функцией фильтрации данных
    """
    # указываем модель
    model = Tightening
    # указываем файл шаблона
    template_name = 'nutrunners_data/tightenings.html'
    # указываем имя контекста для работы в шаблоне
    context_object_name = 'tightings'
    # указываем фильтр для данного представления
    filterset_class = TighteningFilter
    # сортировка данных
    ordering = ['-time_of_creation']

    def get_context_data(self, **kwargs):
        """
        добавляем данные в контекст
        :param kwargs:
        :return:
        """
        # получаем контекст
        context = super().get_context_data(**kwargs)
        # добавляем новый ключ в контекст с отфильтрованными данными
        context['filter'] = TighteningFilter(self.request.GET, queryset=self.get_queryset())
        # возврат контекста
        return context


class VehicleSearch(FilterView):
    """
    Представление для отображения всех автомобилей с фильтрацией
    """
    # указываем модель
    model = Vehicle
    # указываем файл шаблона
    template_name = 'nutrunners_data/vins.html'
    # указываем имя контекста для работы в шаблоне
    context_object_name = 'vehicles'
    # указываем фильтр для данного представления
    filterset_class = VehicleFilter
    # сортировка данных
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        """
        добавляем данные в контекст
        :param kwargs:
        :return:
        """
        # получаем контекст
        context = super().get_context_data(**kwargs)
        # добавляем новый ключ в контекст с отфильтрованными данными
        context['filter'] = VehicleFilter(self.request.GET, queryset=self.get_queryset())
        # возврат контекста
        return context


def print_check_manually(request, **kwargs):
    """
    Функция ручной печати чека для выбранного автомобиля
    :param request:
    :param kwargs:
    :return:
    """
    # получаем ключ(id) автомобиля
    pk = request.GET.get('pk', )
    # получаем все затяжки автомобиля по его вину
    tightenings = Tightening.objects.filter(vin_id=pk)
    # создаем чек со всеми имеющимися затяжками
    check = _create_a_check(tightenings)
    # отправляем чек на принтер
    _send_file_to_printer(check)
    # возвращаемся на главную страницу
    return redirect('/')


# создание фоновой задачи для проверки и печати чеков с результатами затяжек
t = threading.Thread(target=print_data_from_nutrunners, daemon=True)
t.start()

# t1 = threading.Thread(target=timeout_print_data_from_nutrunners, daemon=True)
# t1.start()
