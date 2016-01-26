from user_metrics.models import Metric, MetricItem


def put_metric(slug, user=None, count=1, **kwargs):
    """ Increment a metric by a given user """

    try:
        metric = Metric.objects.get(slug=slug)
    except Metric.DoesNotExist:
        metric = Metric.objects.create(slug=slug, name=slug)

    MetricItem.objects.create(
        metric = metric,
        user = user,
        count = count
    )

def set_metric(slug, user=None, count=1, **kwargs):
    """ Update a metric by a given user """
    try:
        metric = Metric.objects.get(slug=slug)
    except Metric.DoesNotExist:
        metric = Metric.objects.create(slug=slug, name=slug)

    metric.user = user
    metric.count = count
    metric.save()

