import datetime

from django.contrib import admin

from .models import AdvUser
from .utils import send_activation_notification


def send_activation_notifications(model_admin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)

    model_admin.message_user(request, 'Activation emails were sent')


send_activation_notifications.short_description = 'Sending activation user emails'


class NonActivatedUsersFilter(admin.SimpleListFilter):
    title = 'Already activated?'
    parameter_name = 'act_state'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Activated'),
            ('three_days', 'Not activated for 3 days'),
            ('week', 'Not activated for a week')
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'three_days':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonActivatedUsersFilter, )
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ('send_messages', 'is_active', 'is_activated'),
              ('is_staff', 'is_superuser'),
              'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications, )


admin.site.register(AdvUser)
