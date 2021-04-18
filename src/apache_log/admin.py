from django.contrib import admin

from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

from .models import ApacheLog


class ApacheLogAdmin(admin.ModelAdmin):
    readonly_fields = ('ip_address',)
    search_fields = ('uri', 'ip_address')
    list_display = ('ip_address', 'request_date', 'method', 'response_code', 'response_size', 'uri')
    list_filter = ('response_code', 'method', ('request_date', DateRangeFilter))


admin.site.register(ApacheLog, ApacheLogAdmin)