from datetime import date, timedelta


def get_days_for_month():
    list_of_days = []
    day = date.today()
    day_after_month = day + timedelta(days=31)
    while day_after_month >= day:
        list_of_days.append(day)
        day = day + timedelta(days=1)

    return list_of_days