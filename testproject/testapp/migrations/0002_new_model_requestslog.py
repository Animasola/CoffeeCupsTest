# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RequestsLog'
        db.create_table('testapp_requestslog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('requested_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('request_ip', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('request_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('request_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('testapp', ['RequestsLog'])


    def backwards(self, orm):
        # Deleting model 'RequestsLog'
        db.delete_table('testapp_requestslog')


    models = {
        'testapp.personalinfo': {
            'Meta': {'object_name': 'PersonalInfo'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'other_contacts': ('django.db.models.fields.TextField', [], {}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'testapp.requestslog': {
            'Meta': {'object_name': 'RequestsLog'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_ip': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'request_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'request_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'requested_url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['testapp']