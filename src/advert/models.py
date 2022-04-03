from django.db import models
from django.contrib.auth.models import AbstractUser


from .utilities import get_timestamp_path


class CustomUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Is activated?')
    send_messages = models.BooleanField(default=True, verbose_name='Send messages about new commentaries?')

    def delete(self, *args, **kwargs):
        for advert in self.advert_set.all():
            advert.delete()
        super(CustomUser, self).delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class Rubric(models.Model):
    name = models.CharField(max_length=20, verbose_name='Name')
    order = models.IntegerField(default=0, db_index=True, verbose_name='Order')
    super_rubric = models.ForeignKey('SuperRubric', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Super rubric')


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super(SuperRubricManager, self).get_queryset().filter(super_rubric__isnull=True)


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
        return super(SubRubricManager, self).get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):

    objects = SuperRubricManager()

    def __str__(self):
        return f'{self.super_rubric.name} - {self.name}'

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Sub Rubric'
        verbose_name_plural = 'Sub Rubrics'


class Advert(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')
    content = models.TextField(verbose_name='Description')
    price = models.IntegerField(default=0, verbose_name='Price')
    contacts = models.TextField(verbose_name='Contacts')
    image = models.ImageField(blank=True, null=True, upload_to=get_timestamp_path, verbose_name='Main image')
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name='Author')
    rubric = models.ForeignKey('SubRubric', on_delete=models.PROTECT, verbose_name='Rubric')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Is active?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super(Advert, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Advert'
        verbose_name_plural = 'Adverts'
        ordering = ('-created_at',)


class AdditionalImage(models.Model):
    advert = models.ForeignKey('Advert', on_delete=models.CASCADE, verbose_name='Advert')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Image')

    class Meta:
        verbose_name = 'Additional Image'
        verbose_name_plural = 'Additional Images'
