from user_metrics.models import Metric, MetricItem
from user_metrics.utils import get_backend
from user_metrics.models import Metric, MetricItem, MetricDay, MetricWeek, MetricMonth, MetricQuarter, MetricYear
from user_metrics.utils import week_for_date, month_for_date, quarter_for_date, year_for_date

def put_metric(slug, user=None, count=1, **kwargs):
    """ Increment a metric by a given user """
    backend = get_backend()
    backend.put_metric(slug, user=user, count=count, **kwargs)


def set_metric(slug, user=None, count=1, **kwargs):
    backend = get_backend()
    try:
        backend.set_metric(slug, user=user, count=count, **kwargs)
    except AttributeError:
        raise


def metrics_aggregate_by_user():
    # Aggregate Items
    items = MetricItem.objects.all()

    for item in items:
        # Daily Aggregation
        metric_day, create = MetricDay.objects.get_or_create(
            metric=item.metric,
            user=item.user,
            date_up=item.date_up
        )
        metric_day.count = metric_day.count + item.count
        metric_day.save()

        # Weekly Aggregation
        week_date = week_for_date(item.date_up)
        metric_week, create = MetricWeek.objects.get_or_create(
            metric=item.metric,
            user=item.user,
            date_up=week_date
        )
        metric_week.count = metric_week.count + item.count
        metric_week.save()

        # Monthly aggregation
        month_date = month_for_date(item.date_up)
        metric_month, create = MetricMonth.objects.get_or_create(
            metric=item.metric,
            user=item.user,
            date_up=month_date
        )
        metric_month.count = metric_month.count + item.count
        metric_month.save()

        # Quarter aggregation
        quarter_date = quarter_for_date(item.date_up)
        metric_quarter, create = MetricQuarter.objects.get_or_create(
            metric=item.metric,
            user=item.user,
            date_up=quarter_date
        )
        metric_quarter.count = metric_quarter.count + item.count
        metric_quarter.save()

        # Yearly aggregation
        year_date = year_for_date(item.date_up)
        metric_year, create = MetricYear.objects.get_or_create(
            metric=item.metric,
            user=item.user,
            date_up=year_date
        )
        metric_year.count = metric_year.count + item.count
        metric_year.save()

    # remove all metric items
    items.delete()
