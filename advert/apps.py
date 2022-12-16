from django.apps import AppConfig
from django.dispatch import Signal

from .utils import send_activation_notification


class AdvertConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'advert'
    verbose_name = 'Ads-Board'


user_registered = Signal(providing_args=['instance'])


def user_registered_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registered.connect(user_registered_dispatcher)
