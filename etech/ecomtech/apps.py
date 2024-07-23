from django.apps import AppConfig

class EcomtechConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecomtech'

    def ready(self):
        import ecomtech.signals
