# coding: utf-8

from distutils.dir_util import mkpath
from os.path import join
import hashlib

from django.contrib.contenttypes.models import ContentType
from django.test.client import Client

from .utils import get_watch_instances
from . import world, SSIEXPORT_WWW_PATH


def export_instance(instance):
    from .models import Instance
    dburl = export_url(instance.get_absolute_url())
    ct = ContentType.objects.get_for_model(instance)
    dbinstance, created = \
        Instance.objects.get_or_create(content_type=ct, object_id=instance.pk)
    dburl.instance = dbinstance
    dburl.save()
    return dburl, dbinstance


def export_url(original_url):
    from .models import URL, Template
    world.watch = []
    url = original_url
    if url.endswith("/"):
        url = url[:-1]

    path = join(SSIEXPORT_WWW_PATH, url[1:])
    world.path = path
    mkpath(path)
    shtmlpath = join(url[1:], 'index.shtml')
    shtml = join(SSIEXPORT_WWW_PATH, shtmlpath)
    client = Client()
    response = client.get(url, follow=True)
    content = response.content
    open(shtml, 'w').write(content)
    dburl, created = URL.objects.get_or_create(
        path=original_url,
        defaults={'shtml': shtmlpath})
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
