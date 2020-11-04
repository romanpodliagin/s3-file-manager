# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from file_manager.models import File, Bucket, Directory


class BucketAdmin(admin.ModelAdmin):
    model = Bucket


class DirectoryAdmin(admin.ModelAdmin):
    model = Directory


class FileAdmin(admin.ModelAdmin):
    model = File


admin.site.register(Bucket, BucketAdmin)
admin.site.register(Directory, DirectoryAdmin)
admin.site.register(File, FileAdmin)
