# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'DbActionsLog.action'
        db.alter_column('testapp_dbactionslog', 'action', self.gf('django.db.models.fields.CharField')(max_length=3))

    def backwards(self, orm):

        # Changing field 'DbActionsLog.action'
        db.alter_column('testapp_dbactionslog', 'action', self.gf('django.db.models.fields.CharField')(max_length=15))

    models = {
        'testapp.dbactionslog': {
            'Meta': {'object_name': 'DbActionsLog'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'target_instance': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
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
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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