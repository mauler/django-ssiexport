# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Instance'
        db.create_table(u'ssiexport_instance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'ssiexport', ['Instance'])

        # Adding unique constraint on 'Instance', fields ['object_id', 'content_type']
        db.create_unique(u'ssiexport_instance', ['object_id', 'content_type_id'])

        # Adding model 'Template'
        db.create_table(u'ssiexport_template', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('md5sum', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'ssiexport', ['Template'])

        # Adding model 'URL'
        db.create_table(u'ssiexport_url', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'ssiexport', ['URL'])

        # Adding M2M table for field templates on 'URL'
        db.create_table(u'ssiexport_url_templates', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('url', models.ForeignKey(orm[u'ssiexport.url'], null=False)),
            ('template', models.ForeignKey(orm[u'ssiexport.template'], null=False))
        ))
        db.create_unique(u'ssiexport_url_templates', ['url_id', 'template_id'])

        # Adding M2M table for field instances on 'URL'
        db.create_table(u'ssiexport_url_instances', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('url', models.ForeignKey(orm[u'ssiexport.url'], null=False)),
            ('instance', models.ForeignKey(orm[u'ssiexport.instance'], null=False))
        ))
        db.create_unique(u'ssiexport_url_instances', ['url_id', 'instance_id'])

        # Adding model 'Include'
        db.create_table(u'ssiexport_include', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ssiexport.URL'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ssiexport.Template'])),
        ))
        db.send_create_signal(u'ssiexport', ['Include'])


    def backwards(self, orm):
        # Removing unique constraint on 'Instance', fields ['object_id', 'content_type']
        db.delete_unique(u'ssiexport_instance', ['object_id', 'content_type_id'])

        # Deleting model 'Instance'
        db.delete_table(u'ssiexport_instance')

        # Deleting model 'Template'
        db.delete_table(u'ssiexport_template')

        # Deleting model 'URL'
        db.delete_table(u'ssiexport_url')

        # Removing M2M table for field templates on 'URL'
        db.delete_table('ssiexport_url_templates')

        # Removing M2M table for field instances on 'URL'
        db.delete_table('ssiexport_url_instances')

        # Deleting model 'Include'
        db.delete_table(u'ssiexport_include')


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
            'instances': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ssiexport.Instance']", 'symmetrical': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'templates': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ssiexport.Template']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['ssiexport']