from django.apps import AppConfig


class UserAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_app'

    # configuration for 'user' signals
    # in docs: seems like 'ready' is obligatory name
    def ready(self):
        import user_app.signals
