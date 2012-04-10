# -*- coding: utf-8 -*-
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

        # Adding model 'Project'
        db.create_table('projects_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.TypeChoice'], null=True, blank=True)),
            ('type_detail', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.StatusChoice'], null=True, blank=True)),
            ('stalled', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('phase', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('completion', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('dev_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('website_add', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='project_created_by', null=True, to=orm['auth.User'])),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('last_updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='project_last_updated_by', null=True, to=orm['auth.User'])),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('total_housing_units', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('detached_single_fam', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('townhouse_small_multi_fam', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('med_large_multi_fam', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('age_restricted_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('affordable_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('affordable_comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('group_quarters', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('nonres_dev', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hotel_rooms', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('retail_restaurant_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('office_medical_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('manufacturing_industrial_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('warehouse_trucking_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lab_RandD_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('edu_institution_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('other_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('jobs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('est_emp', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('est_emp_loss', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('jobs_per_1000', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('metero_future_discount_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('current_trends_discount_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('parking_spaces', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('redevelopment', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('cluster_subdivision', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('zoning_tool_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ZoningChoice'], null=True, blank=True)),
            ('as_of_right', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mixed_use', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('total_cost', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('total_cost_allocated_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('mapc_comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(srid=26986)),
            ('taz_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Taz'], to_field='taz_id', null=True, blank=True)),
        ))
        db.send_create_signal('projects', ['Project'])

    def backwards(self, orm):
        # Deleting model 'Town'
        db.delete_table('projects_town')

        # Deleting model 'Taz'
        db.delete_table('projects_taz')

        # Deleting model 'StatusChoice'
        db.delete_table('projects_statuschoice')

        # Deleting model 'ZoningChoice'
        db.delete_table('projects_zoningchoice')

        # Deleting model 'TypeChoice'
        db.delete_table('projects_typechoice')

        # Deleting model 'Project'
        db.delete_table('projects_project')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'projects.project': {
            'Meta': {'object_name': 'Project'},
            'affordable_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'affordable_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'age_restricted_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'as_of_right': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cluster_subdivision': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'completion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_created_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'current_trends_discount_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'detached_single_fam': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dev_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'edu_institution_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'est_emp': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'est_emp_loss': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group_quarters': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hotel_rooms': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'jobs_per_1000': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lab_RandD_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'last_updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_last_updated_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '26986'}),
            'manufacturing_industrial_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mapc_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'med_large_multi_fam': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'metero_future_discount_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mixed_use': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nonres_dev': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'office_medical_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'other_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'parking_spaces': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phase': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'redevelopment': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'retail_restaurant_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'stalled': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.StatusChoice']", 'null': 'True', 'blank': 'True'}),
            'taz_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Taz']", 'to_field': "'taz_id'", 'null': 'True', 'blank': 'True'}),
            'total_cost': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_cost_allocated_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'total_housing_units': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'townhouse_small_multi_fam': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type_detail': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.TypeChoice']", 'null': 'True', 'blank': 'True'}),
            'warehouse_trucking_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'website_add': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zoning_tool_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.ZoningChoice']", 'null': 'True', 'blank': 'True'})
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