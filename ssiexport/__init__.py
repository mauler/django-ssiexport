from django.conf import settings

from .registry import world


SSIEXPORT_WWW_PATH = getattr(settings, "SSIEXPORT_WWW_PATH", "export/www")


class Export(object):

    def get_querysets(self):
        return []

    def get_urls(self):
        return []
