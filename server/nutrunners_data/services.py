"""
Файл для описания бизнес-логики и реализации основных механизмов
обработки данных.
"""
# Импорт библиотеки для работы со временем
import time
from datetime import datetime

# Для формирования PDF
from reportlab.pdfgen import canvas

# Для печати файла
# import win32api
# import win32print

# Импорт моделей
from .models import Tightening, Vehicle, Nutrunner

# Константы для функции печати (указываем путь расположения файлов, установленных для скрытой печати)
GHOSTSCRIPT_PATH = "C:\\GHOSTSCRIPT\\bin\\gswin32.exe"
GSPRINT_PATH = "C:\\GSPRINT\\gsprint.exe"


# def _send_file_to_printer(file):
#     """
#     Отправляет печататься полученный файл на принтер,
#     выбранный как принтер по умолчанию.
#     :param file:
#     :return: True
#     """
#     # получаем принтер, выбранный по умолчанию
#     printer = win32print.GetDefaultPrinter()
#     # запуск печати
#     win32api.ShellExecute(
#         0,
#         'open',
#         GSPRINT_PATH,
#         '-ghostscript "'
#         + GHOSTSCRIPT_PATH
#         + '" -printer "'
#         + printer
#         + '" "'
#         + file  # файл, который принемает функция
#         + '" ', '.', 0
#     )
#     print("***** file successfully sent to print *****")
#     return True


def _get_print_data():
    """
    Ищет не напечатанные результаты и формирует данные для печати чека.
    :return: список объектов для печати
    """
    # получаем список всех не напечатанных результатов заяжек
    printable_results = Tightening.objects.filter(printing=False)
    # если есть не напечатанные результаты затяжек:
    if printable_results:
        # для каждого результата в полученном списке
        for result in printable_results:
            # выдергиваем вин
            result_vin = result.vin
            # получаем все затяжки для выбранного вина
            check_data = printable_results.filter(vin=result_vin)
            # если полученые данные удовлетворяют условия печати:
            if verification(check_data):
                print("***** print data received *****")
                # возвращаем список затяжек
                return check_data
            # для тестов (временно!)
            elif len(check_data) == 8:  # цифрой задаем количество результатов для каждого vin
                print("***** print data received *****")
                return check_data
            # иначе продолжаем искать данные, которые подходят по условиям
            else:
                continue


def verification(tightings_list):
    """
    Проверка того, что все гайковерты прислали результаты затяжек
    :param tightings_list:
    :return: True
    """
    # получаем множество всех гайковертов, которые установлены на линии "мазда"
    mazda_nutrunners = set(Nutrunner.objects.filter(production_line=1))
    # получаем множество всех гайковертов, которые установлены на линии "с200"
    c200_nutrunners = set(Nutrunner.objects.filter(production_line=2))
    # формируем пустое множество гайковертов
    nutrunners = set()
    # для каждой затяжки из полученного списка
    for tightening in tightings_list:
        # добовляем гйковерт в множество
        nutrunners.add(tightening.nutrunner)
    # если все гайковерты с линии "мазда" прислали результаты затяжек
    if nutrunners == mazda_nutrunners:
        print("***** verification completed *****")
        # возвращаем истину
        return True
    # а еще если все гайковерты с линии "с200" прислали результаты затяжек
    elif nutrunners == c200_nutrunners:
        print("***** verification completed *****")
        # так же возвращаем истину
        return True
    # иначе ложь
    else:
        return False


def _create_a_check(tightings):
    """
    Формирует чек с результатами затяжек, полученных объектов.
    Возвращает pdf-файл, готовый для печати
    """
    # формирование даты и времени для чека
    now = datetime.now()  # получаем текущее время
    date_string = now.strftime("%d/%m/%Y")  # дата
    time_string = now.strftime("%H:%M")  # время

    # создание объекта PDF
    file_name = 'check.pdf'  # имя файла
    p = canvas.Canvas(file_name)  # создаем пустой лист (холст)
    p.setFont("Times-Roman", 12)  # задаем шрифт и размер

    # получение объекта Vehicle
    vehicle = Vehicle.objects.get(pk=tightings[0].vin_id)

    # выдергиваем вин
    vin = vehicle.vin_number

    # выдергиваем модель
    model = vehicle.model

    # координаты начальной точки файла pdf (верхний левый угол)
    x = 25
    y = 700
    # координата для заголовка
    y_header = 725
    # шаг для координаты х
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
        # получаем дату и врея затяжки
        tightening_datetime = datetime.strftime(tightening.time_of_creation, "%d.%m.%Y/%H:%M:%S")
        # печатаем дату и время затяжки
        p.drawString(x, y - 35, f" Date/Time: {tightening_datetime}")
        p.drawString(x, y - 50, f'{"-" * 138}')
        # если данные о моменте затяжке есть
        if tightening.torque_1:
            # формируем координаты для начала печати
            x1 = x + x_step
            x2 = x1 + 15
            # печать номера затяжки
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
        # меняем статус затяжки (напечатано)
        tightening.printing = True
        # сохраняем изменения в БД
        tightening.save()
        # спускаемся на строку вниз
        y -= 75
        # меняем статус чека для вина (напечатан)
        vehicle.check_printed = True
        # сохраняем изменения в БД
        vehicle.save()
    # сохраняем файл
    p.save()
    print("***** check successfully generated *****")
    # возвращаем имя файла
    return file_name


def print_data_from_nutrunners():
    """
    Функция печати результатов затяжек с гайковертов
    :return:
    """
    # в бесконечном цикле
    while True:
        # через заданное время
        time.sleep(3)
        # проверяем наличие данных для печати и если они появились
        if _get_print_data():
            # получаем эти данные
            results = _get_print_data()
            # формируем для них чек (pdf файл)
            check = _create_a_check(results)
            # отправляем чек на печать
            _send_file_to_printer(check)


def timeout_print_data_from_nutrunners():
    """
    Тестовый вариант функции печати по истечению такт-тайма
    пока не работает
    :return:
    """
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
