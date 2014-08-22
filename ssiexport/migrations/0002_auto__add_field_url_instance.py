# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'URL.instance'
        db.add_column(u'ssiexport_url', 'instance',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='instance_url_set', null=True, to=orm['ssiexport.Instance']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'URL.instance'
        db.delete_column(u'ssiexport_url', 'instance_id')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ssiexport.include': {
            'Meta': {'object_name': 'Include'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ssiexport.Template']"}),
            'url': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ssiexport.URL']"})
        },
        u'ssiexport.instance': {
            'Meta': {'unique_together': "(('object_id', 'content_type'),)", 'object_name': 'Instance'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'ssiexport.template': {
            'Meta': {'object_name': 'Template'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5sum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        u'ssiexport.url': {
            'Meta': {'object_name': 'URL'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instance_url_set'", 'null': 'True', 'to': u"orm['ssiexport.Instance']"}),
            'instances': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ssiexport.Instance']", 'symmetrical': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'templates': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ssiexport.Template']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['ssiexport']