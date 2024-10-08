from django.apps import AppConfig


class AuthusersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authusers'

    def ready(self):
        import authusers.signals  # Import the signals module
