seconds_per_unit = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'y': 31536000}


def convert_to_seconds(time: str) -> int:
    """Conver date like 1d 1y 30d 1m to seconds."""
    try:
        return int(time[:-1]) * seconds_per_unit[time[-1]]
    except (ValueError, KeyError) as e:
        raise ValueError('Wrong time format') from e


def clear_none_from_list(list_: list) -> list:
    """Clear None from list."""
    return [item for item in list_ if item is not None]


ONE_HOUR_SECONDS = 3600
ONE_DAY_SECONDS = ONE_HOUR_SECONDS * 24
ONE_MOUNTH_SECOND = ONE_DAY_SECONDS * 30
ONE_YEAR_SECOND = ONE_MOUNTH_SECOND * 12


def human_time(seconds: int) -> str:
    years = int(seconds // ONE_YEAR_SECOND)
    if years > 0:
        hours_word = num_to_words(years, word_forms=('год', 'года', 'лет'))
        return f'{years} {hours_word}'

    month = int(seconds // ONE_MOUNTH_SECOND)
    if month > 0:
        hours_word = num_to_words(month, word_forms=('месяц', 'месяца', 'месяцев'))
        return f'{month} {hours_word}'

    days = int(seconds // ONE_DAY_SECONDS)
    if days > 0:
        hours_word = num_to_words(days, word_forms=('день', 'дня', 'дней'))
        return f'{days} {hours_word}'

    text = ''
    hours = int(seconds // ONE_HOUR_SECONDS)
    if hours > 0:
        hours_word = num_to_words(hours, word_forms=('час', 'часа', 'часов'))
        text += f'{hours} {hours_word}'

    minutes = int((seconds - hours * ONE_HOUR_SECONDS) // 60)
    if minutes > 0:
        minutes_word = num_to_words(minutes, word_forms=('минута', 'минуты', 'минут'))
        text += f' {minutes} {minutes_word}'

    if text == '':
        seconds_text = num_to_words(seconds, word_forms=('секунда', 'секунды', 'секунд'))
        return f'{int(seconds)} {seconds_text}'

    return text


def num_to_words(count: int, word_forms: tuple[str, str, str]) -> str:
    if count % 10 == 1 and count % 100 != 11:
        p = 0
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        p = 1
    else:
        p = 2
    return word_forms[p]
