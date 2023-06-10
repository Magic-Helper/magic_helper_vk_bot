from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from app.core.constants import DAY_WORK_MONTH_END

ONE_HOUR_SECONDS = 3600
ONE_DAY_SECONDS = ONE_HOUR_SECONDS * 24
ONE_MOUNTH_SECOND = ONE_DAY_SECONDS * 30
ONE_YEAR_SECOND = ONE_MOUNTH_SECOND * 12


def get_work_month_interval() -> tuple[float, float]:
    now = datetime.now()
    if now.day >= DAY_WORK_MONTH_END:
        start = now.replace(day=DAY_WORK_MONTH_END)
        end = now + timedelta(days=1)
    else:
        start = (now - relativedelta(month=1)).replace(day=DAY_WORK_MONTH_END)
        end = now
    return start.timestamp(), end.timestamp()


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
    if count % 10 == 1 and count % 100 != 11:  # noqa
        p = 0
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):  # noqa
        p = 1
    else:
        p = 2
    return word_forms[p]
