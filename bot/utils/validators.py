import re
from datetime import datetime, time as dt_time


def normalize_phone_number(phone_number: str):
    """
    Функция для форматирования номера телефона
    :param phone_number: str: номер телефона
    :return: str: номер телефона в формате +7 (961) 993 - 33 - 16
    """
    cleaned_number = re.sub(r'\D', '', phone_number)

    formatted_number = re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})', r'+7 (\2) \3 - \4 - \5', cleaned_number)

    return formatted_number


def validate_phone_number(phone_number: str):
    """
    Функция для проверки корректности номера телефона
    :param phone_number: str: номер телефона
    :return: bool
    """
    cleaned_number = re.sub(r'\D', '', phone_number)

    pattern = re.compile(r'^(8|\+?7)?(\d{10})$')
    if pattern.match(cleaned_number):
        return True
    else:
        return False


def validate_date(date: str):
    """
    Функция для валидации даты
    :param date:
    :return: tuple (bool, datetime или None)
    """
    try:
        date_obj = datetime.strptime(date, "%d.%m.%Y").date()
        return True, date_obj
    except ValueError:
        return False, None


def validate_time(time: str):
    """
    Функция для валидации времени в формате чч:мм
    :param time: строка с временем
    :return: tuple (bool, datetime или None)
    """
    try:
        time_obj = datetime.strptime(time, "%H:%M").time()
        return True, time_obj
    except ValueError:
        return False, None


def check_date_period(date: datetime.date):
    """
    Функция для проверки даты, является ли она прошедшей
    :param date: строка с датой
    :return: bool
    """
    if date > datetime.now().date():
        return True
    else:
        return False


def check_period(date: datetime.date, time: datetime.time, ):
    """
    Функция для проверки периода, является ли она прошедшим.
    Так же происходит проверка времени в соответствии с рабочими часами с 9:00 до 22:00
    :param date: строка с датой
    :param time: строка c временем
    :return: bool
    """
    try:
        datetime_obj = datetime.combine(date, time)
        now = datetime.now()

        if datetime_obj <= now:
            return False

        work_start = dt_time(9, 0)
        work_end = dt_time(22, 0)
        if time < work_start or time > work_end:
            return False

        return True
    except ValueError:
        return False
