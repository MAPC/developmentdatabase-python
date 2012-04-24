# encoding: utf-8
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

        # Deleting field 'Project.taz'
        db.delete_column('projects_project', 'taz_id')

        # Deleting field 'Project.hd_singlefam_units'
        db.delete_column('projects_project', 'hd_singlefam_units')

        # Deleting field 'Project.hd_mixeduse'
        db.delete_column('projects_project', 'hd_mixeduse')

        # Deleting field 'Project.compl_date'
        db.delete_column('projects_project', 'compl_date')

        # Deleting field 'Project.confirmed'
        db.delete_column('projects_project', 'confirmed')

        # Deleting field 'Project.comments'
        db.delete_column('projects_project', 'comments')

        # Deleting field 'Project.located'
        db.delete_column('projects_project', 'located')

        # Deleting field 'Project.ed_type'
        db.delete_column('projects_project', 'ed_type')

        # Deleting field 'Project.status'
        db.delete_column('projects_project', 'status')

        # Deleting field 'Project.zoning_tool'
        db.delete_column('projects_project', 'zoning_tool')

        # Deleting field 'Project.ed_jobs'
        db.delete_column('projects_project', 'ed_jobs')

        # Deleting field 'Project.located_by'
        db.delete_column('projects_project', 'located_by')

        # Deleting field 'Project.hd_attached_units'
        db.delete_column('projects_project', 'hd_attached_units')

        # Deleting field 'Project.hd_cluster'
        db.delete_column('projects_project', 'hd_cluster')

        # Deleting field 'Project.removed'
        db.delete_column('projects_project', 'removed')

        # Deleting field 'Project.confirmed_by'
        db.delete_column('projects_project', 'confirmed_by')

        # Deleting field 'Project.hd_apt_units'
        db.delete_column('projects_project', 'hd_apt_units')

        # Deleting field 'Project.ed_sqft'
        db.delete_column('projects_project', 'ed_sqft')

        # Deleting field 'Project.hd_over55'
        db.delete_column('projects_project', 'hd_over55')

        # Adding field 'Project.description'
        db.add_column('projects_project', 'description', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.type_id'
        db.add_column('projects_project', 'type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.TypeChoice'], null=True, blank=True), keep_default=False)

        # Adding field 'Project.type_detail'
        db.add_column('projects_project', 'type_detail', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.status_id'
        db.add_column('projects_project', 'status_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.StatusChoice'], null=True, blank=True), keep_default=False)

        # Adding field 'Project.stalled'
        db.add_column('projects_project', 'stalled', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.phase'
        db.add_column('projects_project', 'phase', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.completion'
        db.add_column('projects_project', 'completion', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.dev_name'
        db.add_column('projects_project', 'dev_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.website'
        db.add_column('projects_project', 'website', self.gf('django.db.models.fields.URLField')(max_length=1000, null=True, blank=True), keep_default=False)

        # Adding field 'Project.website_add'
        db.add_column('projects_project', 'website_add', self.gf('django.db.models.fields.URLField')(max_length=1000, null=True, blank=True), keep_default=False)

        # Adding field 'Project.created_by'
        db.add_column('projects_project', 'created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='project_created_by', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Project.create_date'
        db.add_column('projects_project', 'create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.date(2012, 4, 16), blank=True), keep_default=False)

        # Adding field 'Project.last_updated_by'
        db.add_column('projects_project', 'last_updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='project_last_updated_by', null=True, to=orm['auth.User']), keep_default=False)

        # Adding field 'Project.total_housing_units'
        db.add_column('projects_project', 'total_housing_units', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.detached_single_fam'
        db.add_column('projects_project', 'detached_single_fam', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.townhouse_small_multi_fam'
        db.add_column('projects_project', 'townhouse_small_multi_fam', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.med_large_multi_fam'
        db.add_column('projects_project', 'med_large_multi_fam', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.age_restricted_pct'
        db.add_column('projects_project', 'age_restricted_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.affordable_pct'
        db.add_column('projects_project', 'affordable_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.affordable_comment'
        db.add_column('projects_project', 'affordable_comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.group_quarters'
        db.add_column('projects_project', 'group_quarters', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.nonres_dev'
        db.add_column('projects_project', 'nonres_dev', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.hotel_rooms'
        db.add_column('projects_project', 'hotel_rooms', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.retail_restaurant_pct'
        db.add_column('projects_project', 'retail_restaurant_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.office_medical_pct'
        db.add_column('projects_project', 'office_medical_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.manufacturing_industrial_pct'
        db.add_column('projects_project', 'manufacturing_industrial_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.warehouse_trucking_pct'
        db.add_column('projects_project', 'warehouse_trucking_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.lab_RandD_pct'
        db.add_column('projects_project', 'lab_RandD_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.edu_institution_pct'
        db.add_column('projects_project', 'edu_institution_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.other_pct'
        db.add_column('projects_project', 'other_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.jobs'
        db.add_column('projects_project', 'jobs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.est_emp'
        db.add_column('projects_project', 'est_emp', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.est_emp_loss'
        db.add_column('projects_project', 'est_emp_loss', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.jobs_per_1000'
        db.add_column('projects_project', 'jobs_per_1000', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.metero_future_discount_pct'
        db.add_column('projects_project', 'metero_future_discount_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.current_trends_discount_pct'
        db.add_column('projects_project', 'current_trends_discount_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.parking_spaces'
        db.add_column('projects_project', 'parking_spaces', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.cluster_subdivision'
        db.add_column('projects_project', 'cluster_subdivision', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.zoning_tool_id'
        db.add_column('projects_project', 'zoning_tool_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ZoningChoice'], null=True, blank=True), keep_default=False)

        # Adding field 'Project.as_of_right'
        db.add_column('projects_project', 'as_of_right', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.mixed_use'
        db.add_column('projects_project', 'mixed_use', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.total_cost'
        db.add_column('projects_project', 'total_cost', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.total_cost_allocated_pct'
        db.add_column('projects_project', 'total_cost_allocated_pct', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.comment'
        db.add_column('projects_project', 'comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.mapc_comment'
        db.add_column('projects_project', 'mapc_comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.taz_id'
        db.add_column('projects_project', 'taz_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Taz'], to_field='taz_id', null=True, blank=True), keep_default=False)

        # Changing field 'Project.name'
        db.alter_column('projects_project', 'name', self.gf('django.db.models.fields.CharField')(max_length=1000))


    def backwards(self, orm):
        
        # Deleting model 'StatusChoice'
        db.delete_table('projects_statuschoice')

        # Deleting model 'ZoningChoice'
        db.delete_table('projects_zoningchoice')

        # Deleting model 'TypeChoice'
        db.delete_table('projects_typechoice')

        # User chose to not deal with backwards NULL issues for 'Project.taz'
        raise RuntimeError("Cannot reverse this migration. 'Project.taz' and its values cannot be restored.")

        # Adding field 'Project.hd_singlefam_units'
        db.add_column('projects_project', 'hd_singlefam_units', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.hd_mixeduse'
        db.add_column('projects_project', 'hd_mixeduse', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Project.compl_date'
        db.add_column('projects_project', 'compl_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.confirmed'
        db.add_column('projects_project', 'confirmed', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Project.comments'
        db.add_column('projects_project', 'comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.located'
        db.add_column('projects_project', 'located', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Project.ed_type'
        db.add_column('projects_project', 'ed_type', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'Project.status'
        db.add_column('projects_project', 'status', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True), keep_default=False)

        # Adding field 'Project.zoning_tool'
        db.add_column('projects_project', 'zoning_tool', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True), keep_default=False)

        # Adding field 'Project.ed_jobs'
        db.add_column('projects_project', 'ed_jobs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.located_by'
        db.add_column('projects_project', 'located_by', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True), keep_default=False)

        # Adding field 'Project.hd_attached_units'
        db.add_column('projects_project', 'hd_attached_units', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.hd_cluster'
        db.add_column('projects_project', 'hd_cluster', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Project.removed'
        db.add_column('projects_project', 'removed', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Project.confirmed_by'
        db.add_column('projects_project', 'confirmed_by', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True), keep_default=False)

        # Adding field 'Project.hd_apt_units'
        db.add_column('projects_project', 'hd_apt_units', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.ed_sqft'
        db.add_column('projects_project', 'ed_sqft', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Project.hd_over55'
        db.add_column('projects_project', 'hd_over55', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'Project.description'
        db.delete_column('projects_project', 'description')

        # Deleting field 'Project.type_id'
        db.delete_column('projects_project', 'type_id_id')

        # Deleting field 'Project.type_detail'
        db.delete_column('projects_project', 'type_detail')

        # Deleting field 'Project.status_id'
        db.delete_column('projects_project', 'status_id_id')

        # Deleting field 'Project.stalled'
        db.delete_column('projects_project', 'stalled')

        # Deleting field 'Project.phase'
        db.delete_column('projects_project', 'phase')

        # Deleting field 'Project.completion'
        db.delete_column('projects_project', 'completion')

        # Deleting field 'Project.dev_name'
        db.delete_column('projects_project', 'dev_name')

        # Deleting field 'Project.website'
        db.delete_column('projects_project', 'website')

        # Deleting field 'Project.website_add'
        db.delete_column('projects_project', 'website_add')

        # Deleting field 'Project.created_by'
        db.delete_column('projects_project', 'created_by_id')

        # Deleting field 'Project.create_date'
        db.delete_column('projects_project', 'create_date')

        # Deleting field 'Project.last_updated_by'
        db.delete_column('projects_project', 'last_updated_by_id')

        # Deleting field 'Project.total_housing_units'
        db.delete_column('projects_project', 'total_housing_units')

        # Deleting field 'Project.detached_single_fam'
        db.delete_column('projects_project', 'detached_single_fam')

        # Deleting field 'Project.townhouse_small_multi_fam'
        db.delete_column('projects_project', 'townhouse_small_multi_fam')

        # Deleting field 'Project.med_large_multi_fam'
        db.delete_column('projects_project', 'med_large_multi_fam')

        # Deleting field 'Project.age_restricted_pct'
        db.delete_column('projects_project', 'age_restricted_pct')

        # Deleting field 'Project.affordable_pct'
        db.delete_column('projects_project', 'affordable_pct')

        # Deleting field 'Project.affordable_comment'
        db.delete_column('projects_project', 'affordable_comment')

        # Deleting field 'Project.group_quarters'
        db.delete_column('projects_project', 'group_quarters')

        # Deleting field 'Project.nonres_dev'
        db.delete_column('projects_project', 'nonres_dev')

        # Deleting field 'Project.hotel_rooms'
        db.delete_column('projects_project', 'hotel_rooms')

        # Deleting field 'Project.retail_restaurant_pct'
        db.delete_column('projects_project', 'retail_restaurant_pct')

        # Deleting field 'Project.office_medical_pct'
        db.delete_column('projects_project', 'office_medical_pct')

        # Deleting field 'Project.manufacturing_industrial_pct'
        db.delete_column('projects_project', 'manufacturing_industrial_pct')

        # Deleting field 'Project.warehouse_trucking_pct'
        db.delete_column('projects_project', 'warehouse_trucking_pct')

        # Deleting field 'Project.lab_RandD_pct'
        db.delete_column('projects_project', 'lab_RandD_pct')

        # Deleting field 'Project.edu_institution_pct'
        db.delete_column('projects_project', 'edu_institution_pct')

        # Deleting field 'Project.other_pct'
        db.delete_column('projects_project', 'other_pct')

        # Deleting field 'Project.jobs'
        db.delete_column('projects_project', 'jobs')

        # Deleting field 'Project.est_emp'
        db.delete_column('projects_project', 'est_emp')

        # Deleting field 'Project.est_emp_loss'
        db.delete_column('projects_project', 'est_emp_loss')

        # Deleting field 'Project.jobs_per_1000'
        db.delete_column('projects_project', 'jobs_per_1000')

        # Deleting field 'Project.metero_future_discount_pct'
        db.delete_column('projects_project', 'metero_future_discount_pct')

        # Deleting field 'Project.current_trends_discount_pct'
        db.delete_column('projects_project', 'current_trends_discount_pct')

        # Deleting field 'Project.parking_spaces'
        db.delete_column('projects_project', 'parking_spaces')

        # Deleting field 'Project.cluster_subdivision'
        db.delete_column('projects_project', 'cluster_subdivision')

        # Deleting field 'Project.zoning_tool_id'
        db.delete_column('projects_project', 'zoning_tool_id_id')

        # Deleting field 'Project.as_of_right'
        db.delete_column('projects_project', 'as_of_right')

        # Deleting field 'Project.mixed_use'
        db.delete_column('projects_project', 'mixed_use')

        # Deleting field 'Project.total_cost'
        db.delete_column('projects_project', 'total_cost')

        # Deleting field 'Project.total_cost_allocated_pct'
        db.delete_column('projects_project', 'total_cost_allocated_pct')

        # Deleting field 'Project.comment'
        db.delete_column('projects_project', 'comment')

        # Deleting field 'Project.mapc_comment'
        db.delete_column('projects_project', 'mapc_comment')

        # Deleting field 'Project.taz_id'
        db.delete_column('projects_project', 'taz_id_id')

        # Changing field 'Project.name'
        db.alter_column('projects_project', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'nonres_dev': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'office_medical_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'other_pct': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'parking_spaces': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phase': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'redevelopment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'website': ('django.db.models.fields.URLField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'website_add': ('django.db.models.fields.URLField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
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
