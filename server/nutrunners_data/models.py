from django.db import models


# модель производственных линий
class ProductionLine(models.Model):
    line_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.line_name


# Модель для гайковертов
class Nutrunner(models.Model):
    name = models.CharField(max_length=16, unique=True)
    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Модель описывающая автомобиль
class Vehicle(models.Model):
    vin_number = models.CharField(max_length=18, unique=True)
    model = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.vin_number


# Модель затяжек
class Tightening(models.Model):
    # поле для распознавания гайковертов
    nutrunner = models.ForeignKey(Nutrunner, on_delete=models.CASCADE)
    # Вин-номер автомобиля
    vin = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    # время передачи данных с принтконтроллера
    time_of_creation = models.DateTimeField(auto_now_add=True)
    # статус печати затяжки
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


