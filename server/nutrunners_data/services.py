# Импорт библиотеки для работы со временем
import time
from datetime import datetime

# Для формирования PDF
from reportlab.pdfgen import canvas

# Для печати файла
import win32api
import win32print

# Импорт моделей
from .models import Tightening

# Константы для функции печати
GHOSTSCRIPT_PATH = "C:\\GHOSTSCRIPT\\bin\\gswin32.exe"
GSPRINT_PATH = "C:\\GSPRINT\\gsprint.exe"


def _send_file_to_printer(file):
    """
    Отправляет печататься полученный файл на принтер,
    выбранный как принтер по умолчанию.
    :param file:
    :return: True
    """
    printer = win32print.GetDefaultPrinter()
    win32api.ShellExecute(
        0,
        'open',
        GSPRINT_PATH,
        '-ghostscript "'
        + GHOSTSCRIPT_PATH
        + '" -printer "'
        + printer
        + '" "'
        + file
        + '" ', '.', 0
    )
    print("***** file successfully sent to print *****")
    return True


def _get_print_data():
    """
    Ищет не напечатанные результаты и формирует данные для печати чека.
    :return: список объектов для печати
    """
    printable_results = Tightening.objects.filter(printing=False)
    if printable_results:
        for result in printable_results:
            vin_for_print = result.vin
            data_for_creating_check = printable_results.filter(vin=vin_for_print)
            if len(data_for_creating_check) == 4:  # цифрой задаем количество результатов для каждого vin
                print("***** print data received *****")
                return data_for_creating_check
            else:
                continue


def _create_a_check(tightings):
    """
    Формирует чек с результатами затяжек, полученных объектов.
    Возвращает pdf-файл, готовый для печати
    """
    # формирование даты и времени для чека
    now = datetime.now()
    date_string = now.strftime("%d/%m/%Y")
    time_string = now.strftime("%H:%M")

    # создание объекта PDF
    file_name = 'check.pdf'
    p = canvas.Canvas(file_name)

    # координаты начальной точки файла pdf (верхний левый угол)
    x = 25
    y = 700
    y_header = 725
    x_step = 50

    # циклом проходимся по не отпечатанным объектам
    for tightening in tightings:
        # координата для статуса
        y1 = y - 15
        # выдергиваем вин
        vin = tightening.vin
        # выдергиваем модель
        model = tightening.vin.model
        # вывод в pdf вина
        p.drawString(x, 820, f'VIN: "{vin}"')
        # вывод модели
        p.drawString(x, 805, f'Model: "{model}"')
        # вывод даты
        p.drawString(x, 790, f'Date: {date_string}')
        # вывод времени
        p.drawString(x, 775, f'Time: {time_string}')
        # черта разделения
        p.drawString(x, 765, f'{"_" * 82}')
        # имя файла
        p.drawString(250, 745, f'Nutrunners results')
        # заголовок
        p.drawString(x, y_header, f"Nutrunner")
        # печать имени гайковерта
        p.drawString(x, y, f" {tightening.nutrunner}  ")
        # если данные о моменте затяжке есть
        if tightening.torque_1:
            # формируем координаты для начала печати
            x1 = x + 50
            x2 = x + 65
            # печать номера
            p.drawString(x2, y_header, f" 1 ")
            # печать значения момента
            p.drawString(x1, y, f"  {tightening.torque_1}  ")
            # печать статуса затяжки
            p.drawString(x1, y1, f"  {tightening.status_1}  ")
        if tightening.torque_2:
            x1 = x + 100
            x2 = x + 115
            p.drawString(x2, y_header, f" 2 ")
            p.drawString(x1, y, f"  {tightening.torque_2}  ")
            p.drawString(x1, y1, f"  {tightening.status_2}  ")
        if tightening.torque_3:
            x1 = x + 150
            x2 = x + 165
            p.drawString(x2, y_header, f" 3 ")
            p.drawString(x1, y, f"  {tightening.torque_3}  ")
            p.drawString(x1, y1, f"  {tightening.status_3}  ")
        if tightening.torque_4:
            x1 = x + 200
            x2 = x + 215
            p.drawString(x2, y_header, f" 4 ")
            p.drawString(x1, y, f"  {tightening.torque_4}  ")
            p.drawString(x1, y1, f"  {tightening.status_4}  ")
        if tightening.torque_5:
            x1 = x + 250
            x2 = x + 265
            p.drawString(x2, y_header, f" 5 ")
            p.drawString(x1, y, f"  {tightening.torque_5}  ")
            p.drawString(x1, y1, f"  {tightening.status_5}  ")
        if tightening.torque_6:
            x1 = x + 300
            x2 = x + 315
            p.drawString(x2, y_header, f" 6 ")
            p.drawString(x1, y, f"  {tightening.torque_6}  ")
            p.drawString(x1, y1, f"  {tightening.status_6}  ")
        if tightening.torque_7:
            x1 = x + 350
            x2 = x + 365
            p.drawString(x2, y_header, f" 7 ")
            p.drawString(x1, y, f"  {tightening.torque_7}  ")
            p.drawString(x1, y1, f"  {tightening.status_7}  ")
        if tightening.torque_8:
            x1 = x + 400
            x2 = x + 415
            p.drawString(x2, y_header, f" 8 ")
            p.drawString(x1, y, f"  {tightening.torque_8}  ")
            p.drawString(x1, y1, f"  {tightening.status_8}  ")
        if tightening.torque_9:
            x1 = x + 450
            x2 = x + 465
            p.drawString(x2, y_header, f" 9 ")
            p.drawString(x1, y, f"  {tightening.torque_9}  ")
            p.drawString(x1, y1, f"  {tightening.status_9}  ")
        if tightening.torque_10:
            x1 = x + 500
            x2 = x + 515
            p.drawString(x2, y_header, f" 10 ")
            p.drawString(x1, y, f"  {tightening.torque_10}  ")
            p.drawString(x1, y1, f"  {tightening.status_10}  ")
        tightening.printing = True
        tightening.save()
        y -= 50
    p.save()
    print("***** check successfully generated *****")
    return file_name


def print_data_from_nutrunners():
    while True:
        time.sleep(3)
        if _get_print_data():
            results = _get_print_data()
            check = _create_a_check(results)
            # _send_file_to_printer(check)
