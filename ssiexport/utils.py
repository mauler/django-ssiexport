# coding: utf-8

from distutils.dir_util import mkpath
from os.path import join
import hashlib
import sys

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models.query import QuerySet
from django.db.models import signals
from django.db import models
from django.test.client import Client

from ssiexport.models import Instance, URL, Template
from ssiexport import world, SSIEXPORT_WWW_PATH


def connect_signals():
    for exporter_class in get_exporters():
        exporter = exporter_class()
        for qs in getattr(exporter, "get_querysets", lambda: [])():

            def post_delete_signal(sender, instance, *args, **kwargs):
                return

            def post_save_signal(sender, instance, *args, **kwargs):
                print 'queryset', qs.filter(pk=instance.pk)
                if qs.filter(pk=instance.pk).exists():
                    export_instance(instance)

            signals.post_delete.connect(post_delete_signal, sender=qs.model)
            signals.post_save.connect(post_save_signal, sender=qs.model)


def export_instance(instance):
    dburl = export_url(instance.get_absolute_url())
    ct = ContentType.objects.get_for_model(instance)
    dbinstance, created = \
        Instance.objects.get_or_create(content_type=ct, object_id=instance.pk)
    dburl.instance = dbinstance
    dburl.save()
    return dburl, dbinstance


def export_url(url):
    world.watch = []
    if url.endswith("/"):
        url = url[:-1]

    path = join(SSIEXPORT_WWW_PATH, url[1:])
    world.path = path
    mkpath(path)
    shtml = join(path, 'index.shtml')
    client = Client()
    response = client.get(url, follow=True)
    content = response.content
    open(shtml, 'w').write(content)
    dburl, created = URL.objects.get_or_create(path=url)
    if not created:
        dburl.templates.clear()
    for i in response.templates:
        source = open(i.nodelist[0].source[0].name).read()
        md5sum = hashlib.md5(source).hexdigest()
        dbtemplate, created = \
            Template.objects.get_or_create(
                name=i.name, defaults={'md5sum': md5sum})
        dburl.templates.add(dbtemplate)

    if not created:
        dburl.instances.clear()

    for instance in get_watch_instances():
        dburl.instances.add(instance)

    return dburl


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


def get_watch_instances():
    instances = []
    for obj in getattr(world, 'watch', []):

        if isinstance(obj, models.Model):
            instance = obj
            ct = ContentType.objects.get_for_model(instance)
            dbinstance, created = \
                Instance.objects.get_or_create(
                    content_type=ct, object_id=instance.pk)
            instances.append(dbinstance)

        if isinstance(obj, QuerySet):
            for instance in obj:
                ct = ContentType.objects.get_for_model(instance)
                dbinstance, created = \
                    Instance.objects.get_or_create(
                        content_type=ct, object_id=instance.pk)
                instances.append(dbinstance)
    return set(instances)
