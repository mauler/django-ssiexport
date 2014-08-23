# coding: utf-8

from django.core.management.base import BaseCommand

from ssiexport.monkeypatch import apply_monkeypatch
from ssiexport.utils import export_url, get_exporters, export_instance

from ssiexport import world


world.extends = None


from django.conf import settings


settings.STATIC_URL = "http://127.0.0.1:8666" + settings.STATIC_URL
settings.MEDIA_URL = "http://127.0.0.1:8666" + settings.MEDIA_URL


class Command(BaseCommand):
    help = u"ssiexport"

    def handle(self, *args, **options):
        apply_monkeypatch()

        for exporter_class in get_exporters():

            exporter = exporter_class()
            for url in exporter.get_urls():
                print "URL", url
                export_url(url)

            for qs in getattr(exporter, "get_querysets", lambda: [])():
                for instance in qs:
                    print "Instance", instance
                    export_instance(instance)
