from django.apps import AppConfig

from . import checks  # NOQA


class PgcryptoConfig(AppConfig):
    name = "pgcrypto"
