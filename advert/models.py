from django.db import models

from user.models import AdvUser

from .utils import get_timestamp_path


class Rubric(models.Model):
    name = models.CharField(max_length=32, db_index=True, unique=True, verbose_name='Name')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Order')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Super Rubric')


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Super Rubric'
        verbose_name_plural = 'Super Rubrics'


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        return f'{self.super_rubric.name} - {self.name}'

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Sub Rubric'
        verbose_name_plural = 'Sub Rubrics'


class Advert(models.Model):
    title = models.CharField(max_length=64, verbose_name='Product')
    content = models.TextField(verbose_name='Description')
    price = models.FloatField(default=0, verbose_name='Price')
    contacts = models.TextField(verbose_name='Contacts')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Image')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Author')
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Rubric')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Is Active?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Advert'
        verbose_name_plural = 'Adverts'
        ordering = ('-created_at',)


class AdditionalImage(models.Model):
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, verbose_name='Advert')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Image')

    class Meta:
        verbose_name = 'Additional Image'
        verbose_name_plural = 'Additional Images'


class Comment(models.Model):
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, verbose_name='Advert')
    author = models.CharField(max_length=32, verbose_name='Author')
    content = models.TextField(verbose_name='Content')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Is active?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published')

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
