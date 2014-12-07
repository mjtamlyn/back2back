# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Entry.gold_points'
        db.delete_column('back2back_entry', 'gold_points')

        # Deleting field 'Entry.semi_1_points'
        db.delete_column('back2back_entry', 'semi_1_points')

        # Deleting field 'Entry.bronze_points'
        db.delete_column('back2back_entry', 'bronze_points')

        # Deleting field 'Entry.semi_2_points'
        db.delete_column('back2back_entry', 'semi_2_points')

        # Adding field 'Entry.final_round_seed'
        db.add_column('back2back_entry', 'final_round_seed',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.final_match_1_score'
        db.add_column('back2back_entry', 'final_match_1_score',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.final_match_2_score'
        db.add_column('back2back_entry', 'final_match_2_score',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.final_match_3_score'
        db.add_column('back2back_entry', 'final_match_3_score',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.final_match_4_score'
        db.add_column('back2back_entry', 'final_match_4_score',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.final_match_5_score'
        db.add_column('back2back_entry', 'final_match_5_score',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Entry.gold_points'
        db.add_column('back2back_entry', 'gold_points',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.semi_1_points'
        db.add_column('back2back_entry', 'semi_1_points',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.bronze_points'
        db.add_column('back2back_entry', 'bronze_points',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.semi_2_points'
        db.add_column('back2back_entry', 'semi_2_points',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Entry.final_round_seed'
        db.delete_column('back2back_entry', 'final_round_seed')

        # Deleting field 'Entry.final_match_1_score'
        db.delete_column('back2back_entry', 'final_match_1_score')

        # Deleting field 'Entry.final_match_2_score'
        db.delete_column('back2back_entry', 'final_match_2_score')

        # Deleting field 'Entry.final_match_3_score'
        db.delete_column('back2back_entry', 'final_match_3_score')

        # Deleting field 'Entry.final_match_4_score'
        db.delete_column('back2back_entry', 'final_match_4_score')

        # Deleting field 'Entry.final_match_5_score'
        db.delete_column('back2back_entry', 'final_match_5_score')


    models = {
        'back2back.entry': {
            'Meta': {'object_name': 'Entry'},
            'agb_number': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '20'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'final_match_1_score': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'final_match_2_score': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'final_match_3_score': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'final_match_4_score': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'final_match_5_score': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'final_round_seed': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'first_group_index': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'first_group_number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'first_group_placing': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'first_group_points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'first_group_score': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'second_group_index': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'second_group_number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'second_group_placing': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'second_group_points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'second_group_score': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'seeding': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'back2back.score': {
            'Meta': {'object_name': 'Score'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['back2back.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opponent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'opponent_score_set'", 'null': 'True', 'to': "orm['back2back.Entry']", 'blank': 'True'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'score': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stage': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['back2back']