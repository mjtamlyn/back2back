# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Entry.semi_1_points'
        db.add_column('back2back_entry', 'semi_1_points',
                      self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True),
                      keep_default=False)

        # Adding field 'Entry.semi_2_points'
        db.add_column('back2back_entry', 'semi_2_points',
                      self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True),
                      keep_default=False)

        # Adding field 'Entry.bronze_points'
        db.add_column('back2back_entry', 'bronze_points',
                      self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True),
                      keep_default=False)

        # Adding field 'Entry.gold_points'
        db.add_column('back2back_entry', 'gold_points',
                      self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Entry.semi_1_points'
        db.delete_column('back2back_entry', 'semi_1_points')

        # Deleting field 'Entry.semi_2_points'
        db.delete_column('back2back_entry', 'semi_2_points')

        # Deleting field 'Entry.bronze_points'
        db.delete_column('back2back_entry', 'bronze_points')

        # Deleting field 'Entry.gold_points'
        db.delete_column('back2back_entry', 'gold_points')


    models = {
        'back2back.entry': {
            'Meta': {'object_name': 'Entry'},
            'agb_number': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '20'}),
            'bronze_points': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_group_index': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'first_group_number': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'first_group_placing': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'first_group_points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'first_group_score': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'gold_points': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'second_group_index': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'second_group_number': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'second_group_placing': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'second_group_points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'second_group_score': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'seeding': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'semi_1_points': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'semi_2_points': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        },
        'back2back.score': {
            'Meta': {'object_name': 'Score'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['back2back.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opponent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['back2back.Entry']", 'blank': 'True', 'related_name': "'opponent_score_set'", 'null': 'True'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'score': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stage': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['back2back']