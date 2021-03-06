import os
import uuid
import zipfile
from pathlib import Path

import boto3
from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404

SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
            1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}


class Util():

    def approximate_size(self, size, a_kilobyte_is_1024_bytes=True):
        '''Convert a file size to human-readable form.

        Keyword arguments:
        size -- file size in bytes
        a_kilobyte_is_1024_bytes -- if True (default), use multiples of 1024
                                    if False, use multiples of 1000

        Returns: string

        '''

        if size < 0:
            raise ValueError('number must be non-negative')

        multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
        for suffix in SUFFIXES[multiple]:
            size /= multiple
            if size < multiple:
                return '{0:.1f} {1}'.format(size, suffix)

        raise ValueError('number too large')

    def convert_datetime(self, datetime_obj) -> str:
        return datetime_obj.strftime('%m/%d/%Y %H:%M:%S')

    def get_type(self, filename) -> str:
        return filename.endswith('/') and 'DIR' or 'FILE'
    
    def remove_local_file(self, file_name):
        Path(file_name).unlink()

    def remove_local_dir(self, dir_path):
        os.rmdir(dir_path)

    def get_str_path(self, path: Path, file_name: str) -> str:
        return str(path / file_name)

    def get_aws_key_info(self, key: dict) -> dict:
        key_name = key['Key']
        key_size = self.approximate_size(key['Size'])
        key_last_modified = self.convert_datetime(key['LastModified'])

        key_data = {'name': key_name, 'size': key_size, 'last_modified': key_last_modified,
                    'type': self.get_type(key_name)}

        return key_data

    def get_model_attr_by_kwargs(self, model: models.Model, kwargs: dict, attr_name: str):
        model_object = get_object_or_404(model, **kwargs)
        attr = getattr(model_object, attr_name)
        return attr

    def get_model_by_kwargs(self, model: models.Model, kwargs: dict):
        model_object = get_object_or_404(model, **kwargs)
        return model_object


class S3Helper(Util):
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    aws_storage_bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    aws_file_model_keys_mapping = {'aws_last_modified': 'LastModified', 'aws_size': 'Size'}

    def __init__(self):
        self.s3_client = boto3.client('s3',
                                      aws_access_key_id=self.aws_access_key_id,
                                      aws_secret_access_key=self.aws_secret_access_key)

    def save_file(self, file_obj):
        filename = self.get_str_path(settings.UPLOAD_FILE_PATH, file_obj.name)

        with open(filename, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        return file_obj.name, filename

    def upload_file(self, file_obj, dir_name: str, bucket_name=settings.AWS_STORAGE_BUCKET_NAME) -> str:
        """
        Old Version
        :param file_obj:
        :param dir_name:
        :param bucket_name:
        :return:
        """
        filename, full_filename = self.save_file(file_obj)

        uuid_str = uuid.uuid4()
        s3_filename = f'{dir_name}{uuid_str}__{filename}'
        self.s3_client.upload_file(Filename=full_filename, Key=s3_filename, Bucket=bucket_name)
        self.remove_local_file(full_filename)
        return s3_filename

    def upload_file_obj(self, file_obj, dir_name: str, bucket_name=settings.AWS_STORAGE_BUCKET_NAME) -> str:
        uuid_str = uuid.uuid4()
        s3_filename = f'{dir_name}{uuid_str}__{file_obj.name}'
        self.s3_client.upload_fileobj(Fileobj=file_obj, Key=s3_filename, Bucket=bucket_name)
        return s3_filename

    def upload_zip_file(self, file_obj_data: dict, dir_name: str, bucket_name=settings.AWS_STORAGE_BUCKET_NAME) -> str:
        uuid_str = uuid.uuid4()
        file_obj_name = file_obj_data['file_obj_name']
        s3_filename = f'{dir_name}{uuid_str}__{file_obj_name}'
        self.s3_client.upload_fileobj(Fileobj=file_obj_data['data'], Key=s3_filename, Bucket=bucket_name)
        return s3_filename

    def download_file(self, file_name: str, local_file_name: str, bucket_name=settings.AWS_STORAGE_BUCKET_NAME) -> str:
        local_file_name = self.get_str_path(settings.UPLOAD_FILE_PATH, local_file_name)
        self.s3_client.download_file(Filename=local_file_name, Key=file_name, Bucket=bucket_name)
        return local_file_name

    def delete_file(self, file_name):
        self.s3_client.delete_object(Key=file_name, Bucket=self.aws_storage_bucket_name)

    def rename_file(self, aws_key: str, new_file_name: str):
        self.s3_client.copy_object(Key=new_file_name,
                                   CopySource={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': aws_key},
                                   Bucket=self.aws_storage_bucket_name)
        self.delete_file(aws_key)

    def create_bucket(self, bucket_name):
        self.s3_client.create_bucket(Bucket=bucket_name,
                                     CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})

    def load_dirs(self, bucket_name=settings.AWS_STORAGE_BUCKET_NAME) -> list:
        r = self.s3_client.list_objects(Bucket=bucket_name)
        response = []
        for key in r['Contents']:
            if key['Key'].endswith('/'):
                response.append(self.get_aws_key_info(key))

        return response

    def list_dir_by_name(self, name='', only_dirs=True, bucket_name=settings.AWS_STORAGE_BUCKET_NAME) -> list:
        r = self.s3_client.list_objects(Bucket=bucket_name)
        response = []
        dir_name = f'{name}/'
        for key in r['Contents']:
            key_name = key['Key']
            key_data = self.get_aws_key_info(key)

            if not only_dirs:
                response.append(key_data)
            else:
                if key_name.startswith(dir_name) and (key_name != dir_name):
                    response.append(key_data)

        return response

    def load_objects_by_name(self, name='', only_dirs=True, bucket_name=settings.AWS_STORAGE_BUCKET_NAME) -> dict:
        r = self.s3_client.list_objects(Bucket=bucket_name)
        objects = []
        dir_name = f'{name}/'
        for key in r['Contents']:
            key_name = key['Key']

            if not only_dirs:
                objects.append(key)
            else:
                if key_name.startswith(dir_name) and (key_name != dir_name):
                    objects.append(key)

        return {'objects': objects, 'bucket': r['Name']}

    def create_dir(self, dir_name, bucket_name=settings.AWS_STORAGE_BUCKET_NAME):
        dir_name = f'{dir_name}/'
        self.s3_client.put_object(Bucket=bucket_name, Key=dir_name)
        return dir_name

    def update_file_model_info(self, model: models.Model, update_keys: list, Bucket: models.Model):
        if not update_keys:
            update_keys = [f.name for f in model._meta.fields]

        keys_data = self.load_objects_by_name(only_dirs=False)

        bucket, _ = Bucket.objects.get_or_create(name=keys_data['bucket'])

        for key in keys_data['objects']:
            key['bucket'] = bucket
            if model.aws_key == key['Key']:

                for update_key in update_keys:
                    aws_key_name = self.aws_file_model_keys_mapping.get(update_key, update_key)
                    if not hasattr(model, update_key) or (aws_key_name not in key):
                        continue

                    setattr(model, update_key, key[aws_key_name])
                    model.save()

    def load_zip_file(self, file_obj) -> tuple:
        file_content = self.unpack_zip_file(file_obj)
        return file_content

    def unpack_zip_file(self, file_obj) -> dict:
        try:
            print(f'Trying Load ZIP from `{file_obj.name}`')
            opened = zipfile.ZipFile(file_obj)
            file_obj_data = []
            for zip_filename in opened.infolist():
                content = opened.open(zip_filename.filename)
                if not zip_filename.is_dir():
                    if '/' in zip_filename.filename:
                        dir_name, file_obj_name = zip_filename.filename.rsplit('/', 1)
                        dir_name = f'{dir_name}/'
                    else:
                        file_obj_name = zip_filename.filename
                        dir_name = ''
                    file_obj_data.append({'file_obj_name': file_obj_name, 'data': content, 'dir_name': dir_name})

            return file_obj_data

        except zipfile.BadZipfile:
            return
