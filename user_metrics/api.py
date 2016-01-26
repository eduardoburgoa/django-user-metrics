from user_metrics.models import Metric, MetricItem
from user_metrics.utils import get_backend


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
