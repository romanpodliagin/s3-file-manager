# Generated by Django 3.1.2 on 2020-11-03 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0004_auto_20201101_1724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='bucket',
        ),
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('bucket', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='directories', to='file_manager.bucket')),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='directory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='file_manager.directory'),
        ),
    ]