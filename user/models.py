from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Is activated?')
    send_messages = models.BooleanField(default=True, verbose_name='Send messages about new comments?')

    def delete(self, *args, **kwargs):
        for advert in self.advert_set.all():
            advert.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass
