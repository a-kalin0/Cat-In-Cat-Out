# Generated by Django 4.2.5 on 2023-12-20 19:38

import CICO.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CICO', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cats',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=CICO.models.cat_directory_path),
        ),
        migrations.AddField(
            model_name='cats',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to=CICO.models.cat_directory_path),
        ),
        migrations.AddField(
            model_name='cats',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to=CICO.models.cat_directory_path),
        ),
        migrations.AddField(
            model_name='cats',
            name='image5',
            field=models.ImageField(blank=True, null=True, upload_to=CICO.models.cat_directory_path),
        ),
        migrations.AddField(
            model_name='cats',
            name='image6',
            field=models.ImageField(blank=True, null=True, upload_to=CICO.models.cat_directory_path),
        ),
        migrations.AddField(
            model_name='cats',
            name='string_value1',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='cats',
            name='string_value2',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='cats',
            name='string_value3',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='cats',
            name='string_value4',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='cats',
            name='string_value5',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]