from logging import getLogger
from typing import Optional

from django.conf import settings


def get_logger(name: Optional[str] = None):
    return getLogger(name or __name__)


logger = get_logger(settings.APP.lower())
