import os

from django.conf import settings as django_settings
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix=django_settings.APP.upper(),
    settings_files=[f"{"/".join(os.environ.get("DJANGO_SETTINGS_MODULE").split("."))}.py"],
    load_dotenv=True,
)
