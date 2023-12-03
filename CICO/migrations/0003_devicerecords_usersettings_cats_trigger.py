# Generated by Django 4.2.6 on 2023-10-28 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CICO', '0002_alter_usercico_owneddevice'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceRecords',
            fields=[
                ('recordId', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('event', models.CharField(choices=[('IN', 'Entrée'), ('OUT', 'Sortie')], max_length=3)),
                ('isCat', models.BooleanField()),
                ('deviceId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, to_field='ownedDevice')),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('userId', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('setting1', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cats',
            fields=[
                ('catId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('ownerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('recordId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='CICO.devicerecords')),
                ('catId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CICO.cats')),
            ],
        ),
    ]