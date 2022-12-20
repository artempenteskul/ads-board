from django.contrib import admin

from .models import SubRubric, SuperRubric, Advert, AdditionalImage
from .forms import SubRubricForm


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
    list_display = ('title', 'content', 'author', 'rubric', 'created_at')
    fields = ('title', 'content', 'price',
              ('author', 'rubric'),
              'contacts', 'image', 'is_active')
    inlines = (AdditionalImageInline,)


admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
admin.site.register(Advert, AdvertAdmin)
