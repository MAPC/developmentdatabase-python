# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Town'
        db.create_table('projects_town', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('town_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('town_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=26986)),
        ))
        db.send_create_signal('projects', ['Town'])

        # Adding model 'Taz'
        db.create_table('projects_taz', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taz_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('town_id', self.gf('django.db.models.fields.IntegerField')()),
            ('town_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('x', self.gf('django.db.models.fields.FloatField')()),
            ('y', self.gf('django.db.models.fields.FloatField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=26986)),
        ))
        db.send_create_signal('projects', ['Taz'])

        # Adding model 'Project'
        db.create_table('projects_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Taz'], to_field='taz_id')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('compl_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('redevelopment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hd_singlefam_units', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hd_attached_units', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hd_apt_units', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hd_cluster', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hd_over55', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hd_mixeduse', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('zoning_tool', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('ed_jobs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ed_sqft', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('ed_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('confirmed_by', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('located', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('located_by', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('removed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(srid=26986)),
        ))
        db.send_create_signal('projects', ['Project'])


    def backwards(self, orm):
        
        # Deleting model 'Town'
        db.delete_table('projects_town')

        # Deleting model 'Taz'
        db.delete_table('projects_taz')

        # Deleting model 'Project'
        db.delete_table('projects_project')


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
            'taz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Taz']", 'to_field': "'taz_id'"}),
            'zoning_tool': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['projects']
