from communitycomments.projects.models import Project
# from django.contrib import admin
from django.contrib.gis import admin

admin.site.register(Project, admin.GeoModelAdmin)