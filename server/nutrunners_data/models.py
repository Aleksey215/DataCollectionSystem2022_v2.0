"""
Файл для описания таблиц в БД через модели.
Каждый класс - это модель, то есть одна таблица.
"""
from django.db import models


# модель (таблица) производственных линий
class ProductionLine(models.Model):
    # имя линии - строка с максимальной длинной 32 символа и должно быть уникальным
    line_name = models.CharField(max_length=32, unique=True)

    # переопределяем метод для отображения в админке
    def __str__(self):
        return self.line_name


# Модель (таблица) для гайковертов
class Nutrunner(models.Model):
    # имя гайковерта - строка с максимальной длинной 16 символов, уникальное
    name = models.CharField(max_length=16, unique=True)
    # определяем линию, на которой стоит гайковерт, через связь "один ко многим"
    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE)

    # переопределяем метод для отображения в админке
    def __str__(self):
        return self.name


# Модель (таблица) описывающая автомобиль
class Vehicle(models.Model):
    # ВИН автомобиля - строка в 18 символов, уникальная
    vin_number = models.CharField(max_length=18, unique=True)
    # модель автомобиля - строка в 8 символов, уникальная
    model = models.CharField(max_length=8, unique=True)
    # статус печати чека - логическое поле, по умолчанию - ложь, может быть пустым
    check_printed = models.BooleanField(default=False, blank=True, null=True)

    # переопределяем метод для отображения в админке
    def __str__(self):
        return self.vin_number


# Модель (таблица) затяжек
class Tightening(models.Model):
    # определяем гайковерт, который выполнил затяжку
    nutrunner = models.ForeignKey(Nutrunner, on_delete=models.CASCADE)
    # определяем Вин-номер автомобиля, на котором выполнили затяжку
    vin = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    # время затяжки (передается из принтконтроллеров)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    # статус печати затяжки, по умолчанию - ложь, може быть пустым
    printing = models.BooleanField(default=False, blank=True, null=True)
    # кол-во моментов - это кол-во затяжек на одном гайковерте
    torque_1 = models.FloatField(blank=True, null=True)
    torque_2 = models.FloatField(blank=True, null=True)
    torque_3 = models.FloatField(blank=True, null=True)
    torque_4 = models.FloatField(blank=True, null=True)
    torque_5 = models.FloatField(blank=True, null=True)
    torque_6 = models.FloatField(blank=True, null=True)
    torque_7 = models.FloatField(blank=True, null=True)
    torque_8 = models.FloatField(blank=True, null=True)
    torque_9 = models.FloatField(blank=True, null=True)
    torque_10 = models.FloatField(blank=True, null=True)
    # статус соответствует каждой затяжке
    status_1 = models.CharField(max_length=4, blank=True, null=True)
    status_2 = models.CharField(max_length=4, blank=True, null=True)
    status_3 = models.CharField(max_length=4, blank=True, null=True)
    status_4 = models.CharField(max_length=4, blank=True, null=True)
    status_5 = models.CharField(max_length=4, blank=True, null=True)
    status_6 = models.CharField(max_length=4, blank=True, null=True)
    status_7 = models.CharField(max_length=4, blank=True, null=True)
    status_8 = models.CharField(max_length=4, blank=True, null=True)
    status_9 = models.CharField(max_length=4, blank=True, null=True)
    status_10 = models.CharField(max_length=4, blank=True, null=True)
