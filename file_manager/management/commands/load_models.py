from django.core.management.base import BaseCommand
from file_manager.models import File, Bucket
from file_manager.utils import S3Client

s3_client = S3Client()


class Command(BaseCommand):
    """
    """

    help = 'Load S3 File Models'

    def handle(self, *args, **options):

        keys_data = s3_client.load_objects_by_name(only_dirs=False)
        new_files = []

        bucket, _ = Bucket.objects.get_or_create(name=keys_data['bucket'])

        for key in keys_data['objects']:
            print(f'Creating Model: {key["Key"]}')
            new_file = File(bucket=bucket,
                            aws_key=key['Key'],
                            aws_last_modified=key['LastModified'],
                            aws_size=key['Size'],
                            aws_data_updated=True
                            )
            new_files.append(new_file)
            
        File.objects.bulk_create(new_files)
