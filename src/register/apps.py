from django.apps import AppConfig


class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'

    # ready function enables django sognals to work!!!
    def ready(self):
        import register.signals