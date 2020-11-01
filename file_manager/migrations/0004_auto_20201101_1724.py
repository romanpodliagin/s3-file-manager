# Generated by Django 3.1.2 on 2020-11-01 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0003_auto_20201101_1242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='aws_id',
        ),
        migrations.AddField(
            model_name='file',
            name='aws_data_updated',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='aws_last_modified',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='aws_size',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='bucket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='file_manager.bucket'),
        ),
    ]
