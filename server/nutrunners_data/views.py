import threading

from django.core.cache import cache
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView


# Импорт моделей
from .models import *
# Импорт собственных фильтров
from .filters import TighteningFilter, VehicleFilter
# Импорт функции для печати данных
from .services import print_data_from_nutrunners


class TighteningList(ListView):
    model = Tightening
    template_name = 'nutrunners_data/tightnings.html'
    context_object_name = 'active_tightnings'
    ordering = ['-time_of_creation']  # задаем последовательность отображения по id

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_printed_list'] = Tightening.objects.filter(printing=False)
        return context


class TighteningArchiveList(ListView):
    model = Tightening
    template_name = 'nutrunners_data/archive.html'
    context_object_name = 'archived_tightnings'
    ordering = ['-time_of_creation']  # задаем последовательность отображения по id

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['printed_list'] = Tightening.objects.filter(printing=True)
        return context


class TighteningDetail(DetailView):
    template_name = 'nutrunners_data/tigtening_detail.html'
    queryset = Tightening.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'tightening-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f'tightening-{self.kwargs["pk"]}', obj)
        return obj


class VehicleDetailView(DetailView):
    template_name = 'nutrunners_data/vin_detail.html'
    queryset = Vehicle.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'vehicle-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f'vehicle-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tightings_list'] = Tightening.objects.filter(vin=self.kwargs["pk"])
        return context


class TighteningSearch(FilterView):
    model = Tightening
    template_name = 'nutrunners_data/search.html'
    context_object_name = 'tightings_search'
    filterset_class = TighteningFilter
    ordering = ['-time_of_creation']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TighteningFilter(self.request.GET, queryset=self.get_queryset())
        return context


class VehicleSearch(FilterView):
    model = Vehicle
    template_name = 'nutrunners_data/search_v2.html'
    context_object_name = 'vehicle_search'
    filterset_class = VehicleFilter
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = VehicleFilter(self.request.GET, queryset=self.get_queryset())
        return context


t = threading.Thread(target=print_data_from_nutrunners, daemon=True)
t.start()
