import uuid
import boto3
from django.conf import settings


class S3Client():
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY

    def __init__(self):
        self.s3_client = boto3.client('s3',
                                      aws_access_key_id=self.aws_access_key_id,
                                      aws_secret_access_key=self.aws_secret_access_key)

    def upload_file(self, filename, bucket_name=settings.AWS_STORAGE_BUCKET_NAME):
        uuid_str = uuid.uuid4()
        filename = f'{uuid_str}__{filename}'
        # Key = 'tmp-1/manage.py' Full Path
        self.s3_client.upload_file(Filename=filename, Key='tmp-1/manage.py', Bucket=bucket_name)
        return filename

    def delete_file(self, filename, bucket_name=settings.AWS_STORAGE_BUCKET_NAME):
        self.s3_client.Object(settings.AWS_STORAGE_BUCKET_NAME,  'manage.py').delete()

    def create_bucket(self, bucket_name):
        self.s3_client.create_bucket(Bucket=bucket_name,
                                     CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})

    def list_dir(self, bucket_name=settings.AWS_STORAGE_BUCKET_NAME) -> list:
        r = self.s3_client.list_objects(Bucket=bucket_name)
        response = []
        for key in r['Contents']:
            if key['Key'].endswith('/'):
                response.append(key['Key'])

        return response

    def list_dir_by_name(self, dir_name, bucket_name=settings.AWS_STORAGE_BUCKET_NAME) -> list:
        r = self.s3_client.list_objects(Bucket=bucket_name)
        response = []
        dir_name = f'{dir_name}/'
        for key in r['Contents']:
            key_name = key['Key']
            if key_name.startswith(dir_name) and key_name != dir_name:
                response.append(key_name)

        return response

    def create_dir(self, dir_name, bucket_name=settings.AWS_STORAGE_BUCKET_NAME):
        dir_name = f'{dir_name}/'
        self.s3_client.put_object(Bucket=bucket_name, Key=dir_name)
