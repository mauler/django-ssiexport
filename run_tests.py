#!/usr/bin/env python

import sys

from django.conf import settings


def main():
    settings.configure(
        INSTALLED_APPS=[
            'ssiexport',

            'test_app',

            'django_coverage',

            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.admin',
            'django.contrib.sessions',
        ],
        DATABASE_ENGINE='django.db.backends.sqlite3',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        MEDIA_ROOT='media',
        MEDIA_URL='/media/',
        STATIC_URL="/static/",
        ROOT_URLCONF='test_app.urls',
        DEBUG=True,
        TEMPLATE_DEBUG=True,
        TEST_RUNNER='django_coverage.coverage_runner.CoverageRunner',
    )
    from django.test.utils import get_runner
    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['test_app', 'ssiexport'])
    sys.exit(failures)


if __name__ == '__main__':
    main()
