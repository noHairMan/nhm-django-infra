from django.conf import settings as django_settings
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix=django_settings.APP,
    settings_files=django_settings.SETTINGS_FILES,
    environments=True,
    load_dotenv=True,
)
