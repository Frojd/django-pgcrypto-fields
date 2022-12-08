#! /usr/bin/env python
"""From http://stackoverflow.com/a/12260597/400691."""
import os
import sys

import dj_database_url
import django
from colour_runner.django_runner import ColourRunnerMixin
from django.conf import settings
from django.test.runner import DiscoverRunner

BASEDIR = os.path.dirname(os.path.dirname(__file__))

PUBLIC_PGP_KEY_PATH = os.path.abspath(
    os.path.join(BASEDIR, 'tests/keys/public.key')
)
PRIVATE_PGP_KEY_PATH = os.path.abspath(
    os.path.join(BASEDIR, 'tests/keys/private.key')
)
DIFF_PUBLIC_PGP_KEY_PATH = os.path.abspath(
    os.path.join(BASEDIR, 'tests/keys/public_diff.key')
)
DIFF_PRIVATE_PGP_KEY_PATH = os.path.abspath(
    os.path.join(BASEDIR, 'tests/keys/private_diff.key')
)

DB_CONNECTION_URL = os.environ.get("DB_CONNECTION_URL", "postgres://localhost")

diff_keys = dj_database_url.config(
    default='{}/pgcrypto_fields_diff'.format(DB_CONNECTION_URL)
)

# Cannot chain onto the config() call due to error
diff_keys.update({
    'PUBLIC_PGP_KEY': open(DIFF_PUBLIC_PGP_KEY_PATH, 'r').read(),
    'PRIVATE_PGP_KEY': open(DIFF_PRIVATE_PGP_KEY_PATH, 'r').read(),
    'PGCRYPTO_KEY': 'djangorocks',
})

settings.configure(
    DATABASES={
        'default': dj_database_url.config(
            default='{}/pgcrypto_fields'.format(DB_CONNECTION_URL),
        ),
        'diff_keys': diff_keys,
    },
    INSTALLED_APPS=(
        'pgcrypto',
        "tests.diff_keys",
        'tests',
    ),
    DATABASE_ROUTERS=('dbrouters.TestRouter',),
    MIDDLEWARE_CLASSES=(),
    PUBLIC_PGP_KEY=open(PUBLIC_PGP_KEY_PATH, 'r').read(),
    PRIVATE_PGP_KEY=open(PRIVATE_PGP_KEY_PATH, 'r').read(),
    PGCRYPTO_KEY='ultrasecret',
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
    DEBUG=True,
)
django.setup()


class TestRunner(ColourRunnerMixin, DiscoverRunner):
    """Enable colorised output."""


test_runner = TestRunner(verbosity=1)
failures = test_runner.run_tests(['tests'])
if failures:
    sys.exit(1)
