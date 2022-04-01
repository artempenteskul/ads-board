from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Is activated?')
    send_messages = models.BooleanField(default=True, verbose_name='Send messages about new commentaries?')

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
