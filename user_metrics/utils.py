import datetime

from importlib import import_module

from user_metrics import settings


def get_quarter_number(date, zero_index=False):
    result = (date.month - 1) / 3
    if not zero_index:
        result += 1
    return result


def week_for_date(date):
    return date - datetime.timedelta(days=date.weekday())


def month_for_date(date):
    return date - datetime.timedelta(days=date.day-1)


def quarter_for_date(date):
    quarter_month = get_quarter_number(date) * 3 + 1
    return datetime.date(date.year, quarter_month, 1)


def year_for_date(date):
    return datetime.date(date.year, 1, 1)


def total_weeks_aggregated():
    """
    return total of weeks aggregates to MetricWeek model
    """
    from user_metrics.models import MetricWeek
    try:
        first_week = MetricWeek.objects.all().order_by('-date_up')[0].date_up
    except IndexError:
        first_week = week_for_date(datetime.date.today())
    return (datetime.date.today() - first_week).days / 7


def get_backend():
    backend = import_module(settings.USER_METRICS_BACKEND)
    return backend

