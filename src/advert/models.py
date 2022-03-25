from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Is activated?')
    send_messages = models.BooleanField(default=True, verbose_name='Send messages about new commentaries?')

    class Meta(AbstractUser.Meta):
        pass
