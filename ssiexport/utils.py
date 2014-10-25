# coding: utf-8

import hashlib

from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.db import models
from django.template.loader import get_template


def get_modified_templates():
    from .models import Template
    modified = []
    qs = Template.objects.values_list("md5sum", "name")
    for md5sum, name in qs:
        tpl = get_template(name)
        source = open(tpl.nodelist[0].source[0].name).read()
        current_md5sum = hashlib.md5(source).hexdigest()
        tplqs = \
            Template.objects.filter(name=name).exclude(md5sum=current_md5sum)
        for dbtpl in tplqs:
            modified.append(dbtpl)
    return modified


def get_watch_instances():
    from .models import Instance
    from . import world

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


def get_watch_querysets():
    from . import world

    qss = []
    for obj in getattr(world, 'watch', []):
        if isinstance(obj, QuerySet):
            qss.append(obj)
    return qss
