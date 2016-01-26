Django User Metrics
===================

django app that allows capture application metrics by each user individually, so after you can generate reports with aggregation of results
by day or by week for each user

soon more documentation


Installing
==========

* Install with pip::

    pip install django-user-metrics

* Add ``app_metrics`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS =
        # ...
        'user_metrics',
    )



Usage
==========

* Add metrics:

  from user_metrics.api import metric

  put_metric('Download', user)

* Agregate results:

  python manage.py metrics_aggregate_by_user
