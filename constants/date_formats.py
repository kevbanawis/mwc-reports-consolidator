from datetime import datetime

current_date = datetime.today()  # base-date

current_day_number = current_date.strftime("%d")  # 01, 02, .. 31

current_year = current_date.year  # 2021, 2023
month_word = current_date.strftime("%B")  # January, February .. December
month_word_upper = month_word.upper()  # JANUARY, FEBRUARY .. DECEMBER
month_number = current_date.strftime("%m")  # 01, 02, .. 12

month_decimal = current_date.month  # 1, 2, .. 12
day_decimal = current_date.day  # 1, 2, .. 31

__all__ = dict(
    current_day_number=current_day_number,
    current_year=current_year,
    month_word_upper=month_word_upper,
    month_word=month_word,
    month_number=month_number,
    month_decimal=month_decimal,
    day_decimal=day_decimal,
)
