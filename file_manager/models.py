# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from file_manager.utils import S3Client

s3_client = S3Client()


class Bucket(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'<{self.name}>'


class File(models.Model):
    bucket = models.ForeignKey(Bucket, related_name='files', on_delete=models.CASCADE, null=True)
    aws_key = models.CharField(max_length=128)
    aws_last_modified = models.DateTimeField(null=True)
    aws_size = models.BigIntegerField(null=True)
    aws_data_updated = models.BooleanField(null=True)

    def __str__(self):
        return f'{self.bucket} <{self.aws_key}>'

    @property
    def type(self) -> str:
        return self.aws_key.endswith('/') and 'DIR' or 'FILE'

    @property
    def size(self) -> str:
        return s3_client.approximate_size(self.aws_size)

    @property
    def last_modified(self) -> str:
        return self.aws_last_modified.strftime('%m/%d/%Y %H:%M:%S')

    def is_updated(self):
        return self.aws_data_updated and True or False

    def update_attrs(self, update_keys: list):
        if not self.is_updated():
            s3_client.update_file_model_info(self, update_keys, Bucket)
            self.aws_data_updated = True
            self.save()
