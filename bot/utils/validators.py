import re


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
