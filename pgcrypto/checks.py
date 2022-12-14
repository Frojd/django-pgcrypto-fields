import django.apps
from django.conf import settings
from django.core.checks import Error, register

from .mixins import PGPPublicKeyFieldMixin, PGPSymmetricKeyFieldMixin


@register()
def check_required_settings_exist(app_configs, **kwargs):
    """Make sure PGCRYPTO_KEY/PUBLIC_PGP_KEY/PRIVATE_PGP_KEY are set."""
    all_models = django.apps.apps.get_models()
    errors = []

    has_pgp_symmetric_field = _contains_pgp_symmetric_field(all_models)
    if has_pgp_symmetric_field:
        found_keys = [
            getattr(settings, "PGCRYPTO_KEY", None),
        ]

        db_settings = [*settings.DATABASES.values()]
        found_keys = found_keys + [x.get("PGCRYPTO_KEY", None) for x in db_settings]
        found_keys = list(filter(bool, found_keys))

        if len(found_keys) == 0:
            errors = [
                *errors,
                Error(
                    "Missing PGCRYPTO_KEY setting",
                    id="pgcrypto.E001",
                ),
            ]

    has_pgp_public_field = _contains_pgp_public_key_field(all_models)
    if has_pgp_public_field:
        found_keys = [
            (
                getattr(settings, "PUBLIC_PGP_KEY", None),
                getattr(settings, "PRIVATE_PGP_KEY", None),
            )
        ]

        db_settings = [*settings.DATABASES.values()]
        found_keys = found_keys + [
            (x.get("PUBLIC_PGP_KEY", None), x.get("PRIVATE_PGP_KEY", None))
            for x in db_settings
        ]
        found_keys = list(filter(lambda x: bool(x[0]) and bool(x[1]), found_keys))

        if len(found_keys) == 0:
            errors = [
                *errors,
                Error(
                    "Missing PGCRYPTO_KEY setting",
                    id="pgcrypto.E001",
                ),
            ]

    return errors


def _contains_pgp_symmetric_field(models):
    for model in models:
        for field in model._meta.fields:
            if isinstance(field, PGPSymmetricKeyFieldMixin):
                return True
    return False


def _contains_pgp_public_key_field(models):
    for model in models:
        for field in model._meta.fields:
            if isinstance(field, PGPPublicKeyFieldMixin):
                return True
    return False
