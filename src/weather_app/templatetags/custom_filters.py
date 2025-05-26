from django import template

register = template.Library()


@register.filter
def split(value: str, delimiter: str) -> dict[str, str]:
    """
    Разбивает строку на словарь, используя `delimiter` для разделения элементов.
    Каждый элемент делится на ключ и значение по первому вхождению ':'.
    Если разделитель ':' отсутствует, ключ и значение совпадают.
    """

    result = {}

    for item in value.split(delimiter):
        if ":" in item:
            key_part, _, value_part = item.partition(":")
            result[key_part.strip()] = value_part.strip()
        else:
            cleaned_item = item.strip()
            result[cleaned_item] = cleaned_item

    return result


@register.filter
def get_key(dictionary: dict[str, str], key: str) -> str:
    """
    Возвращает значение из словаря по ключу. Если ключ отсутствует, возвращает сам ключ.
    """

    return dictionary.get(key, key)


@register.filter
def translate_condition(value: str) -> str:
    """
    Переводит состояние погоды на русский язык по точному совпадению ключа.
    Если перевод не найден, возвращает исходное значение.
    """

    conditions = {
        "clear": "ясно",
        "partly-cloudy": "малооблачно",
        "cloudy": "облачно",
        "overcast": "пасмурно",
        "rain": "дождь",
        "light-rain": "небольшой дождь",
        "heavy-rain": "сильный дождь",
        "snow": "снег",
        "light-snow": "небольшой снег",
        "thunderstorm": "гроза",
    }

    return conditions.get(value, value)
