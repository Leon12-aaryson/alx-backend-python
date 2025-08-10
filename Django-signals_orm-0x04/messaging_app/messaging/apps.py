from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    def ready(self):
        """
        Import and register signals when the app is ready.
        This ensures that all signal handlers are properly connected.
        """
        import messaging.signals
