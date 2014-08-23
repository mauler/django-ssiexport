# coding: utf-8

from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import get_storage_class
from django.db import models

from __init__ import SSIEXPORT_WWW_PATH


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
