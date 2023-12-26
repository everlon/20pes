from django.apps import AppConfig


class ImoveisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'imoveis'


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import signals