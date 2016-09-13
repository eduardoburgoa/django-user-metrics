import datetime
from django.core.management.base import NoArgsCommand

from user_metrics.api import metrics_aggregate_by_user

class Command(NoArgsCommand):
    help = "Aggregate Application Metrics"

    def handle_noargs(self, **options):
        """ Aggregate Metrics by User """
        metrics_aggregate_by_user()
