# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ZipCode'
        db.create_table('development_zipcode', (
            ('id',       self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zipcode',  self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('name',     self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state',    self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()), # where is SRID?
        ))
        db.send_create_signal('development', ['ZipCode'])


    def backwards(self, orm):
        # Deleting model 'ZipCode'
        db.delete_table('development_zipcode')


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
        'development.communitytype': {
            'Meta': {'object_name': 'CommunityType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'development.municipality': {
            'Meta': {'ordering': "['name']", 'object_name': 'Municipality'},
            'communitytype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['development.CommunityType']", 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'muni_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'development.project': {
            'Meta': {'ordering': "['dd_id']", 'object_name': 'Project'},
            'affordable_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'as_of_right': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ch40': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['development.ZoningTool']", 'null': 'True', 'blank': 'True'}),
            'clustosrd': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'commsf': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'complyr': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_created_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'dd_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ddname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dev_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edinstpct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'emploss': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gqpop': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hotelrms': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'indmfpct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'last_modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_last_modified_by'", 'null': 'True', 'to': "orm['auth.User']"}),
            'lgmultifam': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'mapcintrnl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mfdisc': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mxduse': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ofcmdpct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'otheremprat2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'othpct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ovr55': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'parking_spaces': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pctaffall': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'phased': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prjacrs': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'projecttype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['development.ProjectType']", 'null': 'True'}),
            'projecttype_detail': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rdv': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'retpct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rndpct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rptdemp': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'singfamhu': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stalled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['development.ProjectStatus']"}),
            'taz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['development.Taz']", 'null': 'True', 'blank': 'True'}),
            'total_cost': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_cost_allocated_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'totemp': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tothu': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'twnhsmmult': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url_add': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'walkscore': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'whspct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'xcoord': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ycoord': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'development.projectstatus': {
            'Meta': {'object_name': 'ProjectStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'development.projecttype': {
            'Meta': {'ordering': "['order']", 'object_name': 'ProjectType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'development.taz': {
            'Meta': {'ordering': "['taz_id']", 'object_name': 'Taz'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'municipality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['development.Municipality']"}),
            'taz_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'development.zipcode': {
            'Meta': {'ordering': "['zipcode']", 'object_name': 'ZipCode'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'development.zoningtool': {
            'Meta': {'object_name': 'ZoningTool'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['development']