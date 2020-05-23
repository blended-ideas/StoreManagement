# Generated by Django 3.0.6 on 2020-05-23 08:09

import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models

import store_management.report.utils


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpiryReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False,
                                                                verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False,
                                                                      verbose_name='modified')),
                ('file', models.FileField(upload_to=store_management.report.utils.get_expiry_report_file_path)),
                ('no_of_days', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Expiry Report',
                'verbose_name_plural': 'Expiry Reports',
            },
        ),
    ]