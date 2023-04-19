from django.apps import AppConfig


class AppchatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appchat'
    verbose_name = 'Чат'

    def ready(self):
        import appchat.signals
