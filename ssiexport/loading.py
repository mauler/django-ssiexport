import sys

from django.conf import settings


def get_exporters():
    exporters = []
    for app in settings.INSTALLED_APPS:
        module = "%s.export" % app
        try:
            __import__(module)
            module = sys.modules[module]
            exporters += getattr(module, "exporters", [])
        except ImportError:
            pass
    return exporters
