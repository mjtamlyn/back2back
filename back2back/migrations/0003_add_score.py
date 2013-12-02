# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Score'
        db.create_table('back2back_score', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['back2back.Entry'])),
            ('stage', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('opponent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['back2back.Entry'], related_name='opponent_score_set')),
            ('score', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('points', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('back2back', ['Score'])


    def backwards(self, orm):
        # Deleting model 'Score'
        db.delete_table('back2back_score')


    models = {
        'back2back.entry': {
            'Meta': {'object_name': 'Entry'},
            'agb_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "''", 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_group_index': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'first_group_number': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'first_group_placing': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'first_group_points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'first_group_score': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'seeding': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        },
        'back2back.score': {
            'Meta': {'object_name': 'Score'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['back2back.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opponent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['back2back.Entry']", 'related_name': "'opponent_score_set'"}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'score': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stage': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['back2back']