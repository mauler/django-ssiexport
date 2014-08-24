# coding: utf-8

from django.core.management.base import BaseCommand

from ssiexport.loading import get_exporters
from ssiexport.monkeypatch import apply_monkeypatch
from ssiexport.export import export_url, export_instance

from ssiexport import world


world.extends = None


class Command(BaseCommand):
    help = u"Export all content"

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
