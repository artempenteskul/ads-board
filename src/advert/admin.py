import datetime

from django.contrib import admin

from .models import CustomUser, SuperRubric, SubRubric, Advert, AdditionalImage
from .utilities import send_activation_notification
from .forms import SubRubricForm


def send_activation_notifications(model_admin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    model_admin.message_user(request, 'Email were sent')


send_activation_notifications.short_description = 'Sending emails about user activation'


class NonActivatedFilter(admin.SimpleListFilter):
    title = 'Is activated?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Passed'),
            ('threedays', 'Not passed for three days'),
            ('week', 'Not passed for a week')
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False, date_joined__date__lt=d)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonActivatedFilter,)
    fields = (
        ('username', 'email'),
        ('first_name', 'last_name'),
        ('send_messages', 'is_active', 'is_activated'),
        ('is_staff', 'is_superuser'),
        'groups',
        'user_permissions',
        ('last_login', 'date_joined')
    )
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications, )


class SubRubricInline(admin.TabularInline):
    model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class AdvertAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'rubric', 'author', 'created_at')
    fields = (
        'title', 'content', 'price',
        ('rubric', 'author'),
        'contacts', 'image', 'is_active'
    )
    inlines = (AdditionalImageInline,)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
admin.site.register(Advert, AdvertAdmin)
