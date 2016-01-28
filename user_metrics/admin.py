from django.contrib import admin

from user_metrics.models import Metric, MetricItem, MetricDay, MetricWeek, MetricMonth, MetricQuarter, MetricYear
from user_metrics.utils import get_quarter_number
from django.contrib.admin.filters import DateFieldListFilter, AllValuesFieldListFilter, SimpleListFilter



from datetime import date

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class YearListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Month')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'date_up'

    def lookups(self, request, model_admin):
        available_dates = model_admin.model.objects.all().order_by('date_up').values('date_up').distinct()
        lookup = []
        for date in available_dates:
            converted_date = (str(date["date_up"].year), _(str(date["date_up"].year)))
            lookup.append(converted_date)
        tuple(lookup)
        return lookup

    def queryset(self, request, queryset):
        if self.value():
            year = int(self.value())
            next_year = year + 1
            return queryset.filter(date_up__gte=date(int(year), 1, 1), date_up__lt=date(next_year, 1, 1))
        else:
            return queryset


class MonthListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Month')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'date_up'

    def lookups(self, request, model_admin):
        available_dates = model_admin.model.objects.all().order_by('date_up').values('date_up').distinct()
        lookup = []
        for date in available_dates:
            converted_date = (str(date["date_up"].month) + "_" + str(date["date_up"].year), _(date["date_up"].strftime("%B") + "/" + str(date["date_up"].year)))
            lookup.append(converted_date)
        tuple(lookup)
        return lookup

    def queryset(self, request, queryset):
        if self.value():
            m, y = self.value().split('_')
            month, year = int(m), int(y)
            if month < 12:
                next_month = month + 1
                next_year = year
            else:
                next_month = 1
                next_year = year + 1
            return queryset.filter(date_up__gte=date(int(year), int(month), 1), date_up__lt=date(next_year, next_month, 1))
        else:
            return queryset


class MetricAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class MetricItemAdmin(admin.ModelAdmin):
    list_display = ('metric', 'user', 'count', 'date_up')
    list_filter = ('metric', 'user')


class MetricDayAdmin(admin.ModelAdmin):
    list_display = ('metric', 'user', 'count', 'when', )
    list_filter = (MonthListFilter, 'user', 'metric',)

    search_fields = ['metric', 'user__username']

    def when(self, obj):
        return obj.date_up.strftime("%b. %d, %Y")
    when.short_description = u'When'
    when.admin_order_field = 'date_up'


class MetricWeekAdmin(admin.ModelAdmin):
    list_display = ('metric', 'user', 'count', 'when', )
    list_filter = (MonthListFilter, 'user', 'metric',)

    search_fields = ['metric', 'user__username', 'date_up']

    def when(self, obj):
        return u"Week %(week)s of year %(year)s" % {
            'week': obj.date_up.strftime("%U"),
            'year': obj.date_up.strftime("%Y")
        }
    when.short_description = u'When'
    when.admin_order_field = 'date_up'


class MetricMonthAdmin(admin.ModelAdmin):
    list_display = ('metric', 'user', 'count', 'when', )
    list_filter = (MonthListFilter, 'user', 'metric',)

    search_fields = ['metric', 'user__username']

    def when(self, obj):
        return obj.date_up.strftime("%B %Y"),

    when.short_description = u'When'
    when.admin_order_field = 'date_up'


class MetricQuarterAdmin(admin.ModelAdmin):
    list_display = ('metric', 'user', 'count', 'when', )
    list_filter = (YearListFilter, 'user', 'metric',)

    search_fields = ['metric', 'user__username', 'date_up']


    def when(self, obj):
        return u"Quarter %(quarter)s of %(year)s" % {
            'quarter': get_quarter_number(obj.date_up, True),
            'year': obj.date_up.year
        }
    when.short_description = u'When'
    when.admin_order_field = 'date_up'


class MetricYearAdmin(admin.ModelAdmin):
    list_display = ('metric', 'user', 'count', 'when', )
    list_filter = (YearListFilter, 'user', 'metric',)

    search_fields = ['metric', 'user__username', 'date_up']

    def when(self, obj):
        return obj.date_up.strftime('%Y')
    when.short_description = u'When'
    when.admin_order_field = 'date_up'


admin.site.register(Metric, MetricAdmin)
admin.site.register(MetricItem, MetricItemAdmin)
admin.site.register(MetricDay, MetricDayAdmin)
admin.site.register(MetricWeek, MetricWeekAdmin)
admin.site.register(MetricMonth, MetricMonthAdmin)
admin.site.register(MetricQuarter, MetricQuarterAdmin)
admin.site.register(MetricYear, MetricYearAdmin)
