# Generated by Django 3.1.2 on 2020-11-04 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0006_auto_20201103_1713'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='directory',
            unique_together={('bucket', 'name')},
        ),
    ]
