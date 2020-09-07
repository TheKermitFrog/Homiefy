from django.apps import AppConfig
# from django.db.models.signals import post_save
# from django.utils.translation import ugettext_lazy as _
# from .signals import create_timeSlot, save_timeSlot


class MainConfig(AppConfig):
    name = 'main'

    # def ready(self):
    #     service = self.get_model('Service')
    #     post_save.connect(create_timeSlot, sender=service, dispatch_uid="service_identifier")
