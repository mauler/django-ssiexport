# coding: utf-8

from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Instance(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ("object_id", "content_type", )


class Template(models.Model):
    name = models.CharField(db_index=True, max_length=100, unique=True)
    md5sum = models.CharField(max_length=32)


class URL(models.Model):
    path = models.CharField(db_index=True, max_length=255, unique=True)
    templates = models.ManyToManyField("Template")
    instance = models.ForeignKey(
        "Instance",
        null=True,
        related_name="instance_url_set",
    )
    instances = models.ManyToManyField("Instance")


class Include(models.Model):
    url = models.ForeignKey("URL")
    template = models.ForeignKey("Template")
