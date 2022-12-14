# flake8: noqa
from django.conf import settings
from django.test import override_settings, TestCase

from pgcrypto.checks import check_required_settings_exist


class TestChecks(TestCase):
    # noqa: D103
    def test_pgcrypto_key_exist(self):
        errors = check_required_settings_exist(None)
        self.assertEqual(len(errors), 0)

    @override_settings()
    def test_missing_pgcrypto_key_raises_error(self):
        del settings.PGCRYPTO_KEY

        key_value = settings.DATABASES["diff_keys"]["PGCRYPTO_KEY"]
        del settings.DATABASES["diff_keys"]["PGCRYPTO_KEY"]

        errors = check_required_settings_exist(None)
        self.assertEqual(errors[0].id, "pgcrypto.E001")

        settings.DATABASES["diff_keys"]["PGCRYPTO_KEY"] = key_value

    @override_settings()
    def test_error_not_raised_if_key_is_in_db_settings(self):
        del settings.PGCRYPTO_KEY

        errors = check_required_settings_exist(None)
        self.assertEqual(len(errors), 0)

    @override_settings()
    def test_empty_pgcrypto_raises_error(self):
        settings.PGCRYPTO_KEY = None
        key_value = settings.DATABASES["diff_keys"]["PGCRYPTO_KEY"]
        del settings.DATABASES["diff_keys"]["PGCRYPTO_KEY"]

        errors = check_required_settings_exist(None)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].id, "pgcrypto.E001")

        settings.DATABASES["diff_keys"]["PGCRYPTO_KEY"] = key_value

    def test_public_key_exist(self):
        errors = check_required_settings_exist(None)
        self.assertEqual(len(errors), 0)

    @override_settings()
    def test_missing_public_pgp_key_raises_error(self):
        del settings.PUBLIC_PGP_KEY

        key_value = settings.DATABASES["diff_keys"]["PUBLIC_PGP_KEY"]
        del settings.DATABASES["diff_keys"]["PUBLIC_PGP_KEY"]

        errors = check_required_settings_exist(None)
        self.assertEqual(errors[0].id, "pgcrypto.E001")

        settings.DATABASES["diff_keys"]["PUBLIC_PGP_KEY"] = key_value

    @override_settings()
    def test_missing_private_pgp_key_raises_error(self):
        del settings.PRIVATE_PGP_KEY

        key_value = settings.DATABASES["diff_keys"]["PRIVATE_PGP_KEY"]
        del settings.DATABASES["diff_keys"]["PRIVATE_PGP_KEY"]

        errors = check_required_settings_exist(None)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].id, "pgcrypto.E001")

        settings.DATABASES["diff_keys"]["PRIVATE_PGP_KEY"] = key_value
