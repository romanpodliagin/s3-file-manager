# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from file_manager.models import File, Bucket


class FileAdmin(admin.ModelAdmin):
    model = File


class BucketAdmin(admin.ModelAdmin):
    model = Bucket


admin.site.register(File, FileAdmin)
admin.site.register(Bucket, BucketAdmin)
