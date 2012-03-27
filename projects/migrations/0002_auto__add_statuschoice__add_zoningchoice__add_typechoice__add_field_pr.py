# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StatusChoice'
        db.create_table('projects_statuschoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('projects', ['StatusChoice'])

        # Adding model 'ZoningChoice'
        db.create_table('projects_zoningchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('projects', ['ZoningChoice'])

        # Adding model 'TypeChoice'
        db.create_table('projects_typechoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('projects', ['TypeChoice'])

        # Adding field 'Project.status_new'
        db.add_column('projects_project', 'status_new',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.StatusChoice'], null=True),
                      keep_default=False)

        # Adding field 'Project.zoning_tool_new'
        db.add_column('projects_project', 'zoning_tool_new',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ZoningChoice'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.type'
        db.add_column('projects_project', 'type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.TypeChoice'], null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting model 'StatusChoice'
        db.delete_table('projects_statuschoice')

        # Deleting model 'ZoningChoice'
        db.delete_table('projects_zoningchoice')

        # Deleting model 'TypeChoice'
        db.delete_table('projects_typechoice')

        # Deleting field 'Project.status_new'
        db.delete_column('projects_project', 'status_new_id')

        # Deleting field 'Project.zoning_tool_new'
        db.delete_column('projects_project', 'zoning_tool_new_id')

        # Deleting field 'Project.type'
        db.delete_column('projects_project', 'type_id')

    models = {
        'projects.project': {
            'Meta': {'object_name': 'Project'},
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'compl_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'confirmed_by': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'ed_jobs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ed_sqft': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ed_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'hd_apt_units': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hd_attached_units': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hd_cluster': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hd_mixeduse': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hd_over55': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hd_singlefam_units': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'located': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'located_by': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '26986'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'redevelopment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'status_new': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.StatusChoice']", 'null': 'True'}),
            'taz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Taz']", 'to_field': "'taz_id'"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.TypeChoice']", 'null': 'True', 'blank': 'True'}),
            'zoning_tool': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'zoning_tool_new': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.ZoningChoice']", 'null': 'True', 'blank': 'True'})
        },
        'projects.statuschoice': {
            'Meta': {'object_name': 'StatusChoice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'projects.taz': {
            'Meta': {'object_name': 'Taz'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '26986'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'taz_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'town_id': ('django.db.models.fields.IntegerField', [], {}),
            'town_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {})
        },
        'projects.town': {
            'Meta': {'ordering': "['town_name']", 'object_name': 'Town'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '26986'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'town_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'town_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'projects.typechoice': {
            'Meta': {'object_name': 'TypeChoice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'projects.zoningchoice': {
            'Meta': {'object_name': 'ZoningChoice'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['projects']