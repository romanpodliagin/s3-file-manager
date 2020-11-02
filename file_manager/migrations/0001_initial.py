# Generated by Django 3.1.2 on 2020-11-01 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(choices=[('DIR', 'DIR'), ('FILE', 'FILE')], max_length=128)),
                ('aws_key', models.CharField(max_length=128)),
                ('aws_last_modified', models.DateTimeField()),
                ('aws_size', models.CharField(max_length=128)),
                ('aws_id', models.CharField(max_length=128)),
                ('bucket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='file_manager.bucket')),
            ],
        ),
    ]