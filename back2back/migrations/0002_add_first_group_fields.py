# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Entry.first_group_number'
        db.add_column('back2back_entry', 'first_group_number',
                      self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True),
                      keep_default=False)

        # Adding field 'Entry.first_group_index'
        db.add_column('back2back_entry', 'first_group_index',
                      self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True),
                      keep_default=False)

        # Adding field 'Entry.first_group_placing'
        db.add_column('back2back_entry', 'first_group_placing',
                      self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True),
                      keep_default=False)

        # Adding field 'Entry.first_group_points'
        db.add_column('back2back_entry', 'first_group_points',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Entry.first_group_score'
        db.add_column('back2back_entry', 'first_group_score',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Entry.first_group_number'
        db.delete_column('back2back_entry', 'first_group_number')

        # Deleting field 'Entry.first_group_index'
        db.delete_column('back2back_entry', 'first_group_index')

        # Deleting field 'Entry.first_group_placing'
        db.delete_column('back2back_entry', 'first_group_placing')

        # Deleting field 'Entry.first_group_points'
        db.delete_column('back2back_entry', 'first_group_points')

        # Deleting field 'Entry.first_group_score'
        db.delete_column('back2back_entry', 'first_group_score')


    models = {
        'back2back.entry': {
            'Meta': {'object_name': 'Entry'},
            'agb_number': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20', 'default': "''"}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_group_index': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'first_group_number': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'first_group_placing': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'first_group_points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'first_group_score': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'seeding': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['back2back']