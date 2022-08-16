# Импорт библиотеки для работы со временем
import time
from datetime import datetime

# Для формирования PDF
from reportlab.pdfgen import canvas

# Для печати файла
import win32api
import win32print

# Импорт моделей
from .models import Tightening, Vehicle, Nutrunner

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
            result_vin = result.vin
            check_data = printable_results.filter(vin=result_vin)
            if verification(check_data):
                print("***** print data received *****")
                return check_data
            # для тестов (временно!)
            elif len(check_data) == 8:  # цифрой задаем количество результатов для каждого vin
                print("***** print data received *****")
                return check_data
            else:
                continue


def verification(tightings_list):
    """
    Проверка того, что все гайковерты прислали результаты затяжек
    :param tightings_list:
    :return: True
    """
    mazda_nutrunners = set(Nutrunner.objects.filter(production_line=1))
    c200_nutrunners = set(Nutrunner.objects.filter(production_line=2))
    nutrunners = set()
    for tightening in tightings_list:
        nutrunners.add(tightening.nutrunner)
    if nutrunners == mazda_nutrunners:
        print("***** verification completed *****")
        return True
    elif nutrunners == c200_nutrunners:
        print("***** verification completed *****")
        return True
    else:
        return False


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
    p.setFont("Times-Roman", 12)

    # получение объекта Vehicle
    vehicle = Vehicle.objects.get(pk=tightings[0].vin_id)

    # выдергиваем вин
    vin = vehicle.vin_number

    # выдергиваем модель
    model = vehicle.model

    # координаты начальной точки файла pdf (верхний левый угол)
    x = 25
    y = 700
    y_header = 725
    x_step = 50

    # циклом проходимся по не отпечатанным объектам
    for tightening in tightings:
        # координата для статуса
        y1 = y - 15

        # вывод в pdf вина
        p.drawString(x, 820, f'VIN: "{vin}"')
        # вывод модели
        p.drawString(x, 805, f'Model: "{model}"')
        # вывод даты
        p.drawString(x, 790, f'Date: {date_string}')
        # вывод времени
        p.drawString(x, 775, f'Time: {time_string}')
        # имя чека
        p.drawString(250, 745, f'Nutrunners results')
        # заголовок
        p.drawString(x, y_header, f"Nutrunner")
        p.drawString(x, 715, f'{"-" * 138}')
        # печать имени гайковерта
        p.drawString(x, y, f" {tightening.nutrunner}  ")
        tightening_datetime = datetime.strftime(tightening.time_of_creation, "%d.%m.%Y/%H:%M:%S")
        p.drawString(x, y - 35, f" Date/Time: {tightening_datetime}")
        p.drawString(x, y - 50, f'{"-" * 138}')
        # если данные о моменте затяжке есть
        if tightening.torque_1:
            # формируем координаты для начала печати
            x1 = x + x_step
            x2 = x1 + 15
            # печать номера
            p.drawString(x2, y_header, f" 1 ")
            # печать значения момента
            p.drawString(x1, y, f"  {tightening.torque_1}  ")
            # печать статуса затяжки
            p.drawString(x1, y1, f"  {tightening.status_1}  ")
        if tightening.torque_2:
            x1 = x + x_step * 2
            x2 = x1 + 15
            p.drawString(x2, y_header, f" 2 ")
            p.drawString(x1, y, f"  {tightening.torque_2}  ")
            p.drawString(x1, y1, f"  {tightening.status_2}  ")
        if tightening.torque_3:
            x1 = x + x_step * 3
            x2 = x1 + 15
            p.drawString(x2, y_header, f" 3 ")
            p.drawString(x1, y, f"  {tightening.torque_3}  ")
            p.drawString(x1, y1, f"  {tightening.status_3}  ")
        if tightening.torque_4:
            x1 = x + x_step * 4
            x2 = x1 + 15
            p.drawString(x2, y_header, f" 4 ")
            p.drawString(x1, y, f"  {tightening.torque_4}  ")
            p.drawString(x1, y1, f"  {tightening.status_4}  ")
        if tightening.torque_5:
            x1 = x + x_step * 5
            x2 = x1 + 15
            p.drawString(x2, y_header, f" 5 ")
            p.drawString(x1, y, f"  {tightening.torque_5}  ")
            p.drawString(x1, y1, f"  {tightening.status_5}  ")
        if tightening.torque_6:
            x1 = x + x_step * 6
            x2 = x1 + 15
            p.drawString(x2, y_header, f" 6 ")
            p.drawString(x1, y, f"  {tightening.torque_6}  ")
            p.drawString(x1, y1, f"  {tightening.status_6}  ")
        if tightening.torque_7:
            x1 = x + x_step * 7
            x2 = x1 + 15
            p.drawString(x2, y_header, f" 7 ")
            p.drawString(x1, y, f"  {tightening.torque_7}  ")
            p.drawString(x1, y1, f"  {tightening.status_7}  ")
        if tightening.torque_8:
            x1 = x + x_step * 8
            x2 = x1 + 15
            p.drawString(x2, y_header, f" 8 ")
            p.drawString(x1, y, f"  {tightening.torque_8}  ")
            p.drawString(x1, y1, f"  {tightening.status_8}  ")
        if tightening.torque_9:
            x1 = x + x_step * 9
            x2 = x1 + 15
            p.drawString(x2, y_header, f" 9 ")
            p.drawString(x1, y, f"  {tightening.torque_9}  ")
            p.drawString(x1, y1, f"  {tightening.status_9}  ")
        if tightening.torque_10:
            x1 = x + x_step * 10
            x2 = x1 + 15
            p.drawString(x2, y_header, f" 10 ")
            p.drawString(x1, y, f"  {tightening.torque_10}  ")
            p.drawString(x1, y1, f"  {tightening.status_10}  ")
        tightening.printing = True
        tightening.save()
        y -= 75
        vehicle.check_printed = True
        vehicle.save()
    p.save()
    print("***** check successfully generated *****")
    return file_name


def print_data_from_nutrunners():
    while True:
        time.sleep(3)
        if _get_print_data():
            results = _get_print_data()
            check = _create_a_check(results)
            _send_file_to_printer(check)


def timeout_print_data_from_nutrunners():
    while True:
        time.sleep(5)
        print('***** check no printing data *****')
        if Vehicle.objects.filter(check_printed=False):
            vin_for_printing = Vehicle.objects.filter(check_printed=False)[0]
            print(f'***** find vin: {vin_for_printing} *****')
            time.sleep(30)
            current_vin = Vehicle.objects.filter(check_printed=False)[0]
            if vin_for_printing == current_vin:
                print(f'***** time out for {vin_for_printing} *****')
                time_out_results = Tightening.objects.filter(vin=vin_for_printing)
                time_out_check = _create_a_check(time_out_results)
                print(f'***** start print time out check *****')
                # _send_file_to_printer(time_out_check)
            else:
                print(f'***** start new search *****')
                continue
        else:
            continue
