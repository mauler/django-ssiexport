# coding: utf-8

from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import get_storage_class
from django.db.models import manager
from django.db.models import signals
from django.db import models

import bson

from .monkeypatch import apply_manager_monkeypatch
from . import SSIEXPORT_WWW_PATH


manager_init_original = manager.Manager.__init__


def manager_init(self, *args, **kwargs):
    manager_init_original(self, *args, **kwargs)
    apply_manager_monkeypatch(self)

manager.Manager.__init__ = manager_init


# def class_prepared_signal(sender, *args, **kwargs):
#     apply_manager_monkeypatch(sender.objects)


# signals.class_prepared.connect(class_prepared_signal)


class Queryset(models.Model):
    url = models.ForeignKey("URL")
    content_type = models.ForeignKey(ContentType)
    bson_data = models.TextField()

    def get(self):
        objects = self.content_type.model_class().objects
        data = bson.loads(self.bson_data).get('data', [])
        qs = objects
        for chain, args, kwargs in data:
            qs = getattr(qs, chain)
            qs = qs(*args, **kwargs)
        if qs == objects:
            qs = qs.all()
        return qs

    def set(self, qs):
        self.content_type = ContentType.objects.get_for_model(qs.model)
        self.bson_data = bson.dumps({'data': qs._monkeypatch_calls})


class Instance(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ("id", )
        unique_together = ("object_id", "content_type", )

    def __unicode__(self):
        return "%s %s" % (self.content_type, self.object_id)

    @staticmethod
    def get_from_instance(instance):
        ct = ContentType.objects.get_for_model(instance.__class__)
        return ct.instance_set.get(object_id=instance.id)


class Template(models.Model):
    name = models.CharField(db_index=True, max_length=100, unique=True)
    md5sum = models.CharField(max_length=32)

    class Meta:
        ordering = ("id", )

    def __unicode__(self):
        return self.name


class URL(models.Model):
    path = models.CharField(db_index=True, max_length=255, unique=True)
    templates = models.ManyToManyField("Template")
    instance = models.ForeignKey(
        "Instance",
        null=True,
        related_name="instance_url_set",
    )
    instances = models.ManyToManyField("Instance")
    shtml = models.FileField(
        max_length=1024,
        storage=get_storage_class()(SSIEXPORT_WWW_PATH),
        upload_to="other",
    )

    class Meta:
        ordering = ("path", )

    def __unicode__(self):
        return self.path


class Include(models.Model):
    url = models.ForeignKey("URL")
    template = models.ForeignKey("Template")

    class Meta:
        ordering = ("url", 'template',)


from .export import export_instance, export_url
from .loading import get_exporters


for exporter_class in get_exporters():
    exporter = exporter_class()
    for qs in getattr(exporter, "get_querysets", lambda: [])():

        model_class = qs.model

        def post_delete_signal(sender, instance, *args, **kwargs):
            instance = Instance.get_from_instance(instance)
            for dburl in instance.instance_url_set.all():
                dburl.shtml.delete()
                dburl.delete()

            for url in instance.url_set.all():
                export_url(url.path)

            instance.delete()

        signals.post_delete.connect(
            post_delete_signal, sender=model_class)

        def post_save_signal(sender, instance, *args, **kwargs):
            if qs.filter(pk=instance.pk).exists():
                export_instance(instance)

        signals.post_save.connect(
            post_save_signal, sender=model_class)
