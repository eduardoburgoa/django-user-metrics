import datetime
from django.core.management.base import NoArgsCommand

from user_metrics.models import Metric, MetricItem, MetricDay, MetricWeek, MetricMonth, MetricQuarter, MetricYear
from user_metrics.utils import week_for_date, month_for_date, quarter_for_date, year_for_date

from user_metrics.api import metrics_aggregate_by_user

class Command(NoArgsCommand):
    help = "Aggregate Application Metrics"

    def handle_noargs(self, **options):
        """ Aggregate Metrics by User """
        metrics_aggregate_by_user()