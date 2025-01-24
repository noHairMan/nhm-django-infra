from django.apps import AppConfig


class PorscheConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "porsche"

    def ready(self):
        import dynaconf  # noqa
        settings = dynaconf.DjangoDynaconf(__name__)  # noqa
        super().ready()
