import os

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DJANGO",
    settings_files=[f"{"/".join(os.environ.get("DJANGO_SETTINGS_MODULE").split("."))}.py"],
    environments=True,
    load_dotenv=True,
)
