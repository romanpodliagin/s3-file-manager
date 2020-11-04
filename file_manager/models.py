# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timezone

from django.db import models

from file_manager.managers import FileManger
from file_manager.utils import S3Helper

s3_helper = S3Helper()


class Type:
    FILE = 'FILE'
    DIR = 'DIR'

    CHOICES = (
        (FILE, FILE),
        (DIR, DIR)
    )


class Bucket(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'<{self.name}>'


class Directory(models.Model):
    bucket = models.ForeignKey(Bucket, related_name='directories', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=128)
    
    class Meta:
        verbose_name_plural = 'Directories'
        unique_together = ('bucket', 'name')

    def __str__(self):
        return f'<{self.bucket}> <{self.name}>'

    @property
    def last_updated_min(self):
        q = self.files.order_by('-aws_last_modified')
        if q:
            last_file_timestamp = q.first().aws_last_modified
            now = datetime.now(timezone.utc)
            value = (now - last_file_timestamp).seconds
            if value < 60:
                return 1
            return round(value / 60)


class File(models.Model):
    directory = models.ForeignKey(Directory, related_name='files', on_delete=models.CASCADE, null=True)
    aws_key = models.CharField(max_length=128)
    aws_last_modified = models.DateTimeField(null=True)
    aws_size = models.BigIntegerField(null=True)
    aws_data_updated = models.BooleanField(null=True)

    objects = FileManger.as_manager()

    class Meta:
        unique_together = ('directory', 'aws_key')

    def __str__(self):
        return f'{self.directory} <{self.aws_key}>'

    @property
    def type(self) -> str:
        return self.aws_key.endswith('/') and Type.DIR or Type.FILE

    @property
    def ext(self) -> str:
        if self.type == Type.DIR:
            ext = ''
        elif '.' not in self.aws_key:
            ext = ''
        else:
            ext = self.aws_key.rsplit('.', 1)[-1]
            ext = f'.{ext}'
        return ext

    @property
    def size(self) -> str:
        return s3_helper.approximate_size(self.aws_size)

    @property
    def last_modified(self) -> str:
        return self.aws_last_modified.strftime('%m/%d/%Y %H:%M:%S')

    def is_updated(self):
        return self.aws_data_updated and True or False

    def update_attrs(self, update_keys: list):
        if not self.is_updated():
            s3_helper.update_file_model_info(self, update_keys, Bucket)
            self.aws_data_updated = True
            self.save()

    def rename_file(self, new_file_name):
        type_init = self.type
        s3_helper.rename_file(self.aws_key, new_file_name)
        self.aws_key = new_file_name
        if type_init == self.type:
            self.save()
        else:
            return {'msg': 'File Type Conflict.'}

    def delete(self, using=None, keep_parents=False):
        s3_helper.delete_file(self.aws_key)
        return super().delete(using=using, keep_parents=keep_parents)
