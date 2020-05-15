# Generated by Django 3.0.6 on 2020-05-15 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shifts', '0003_auto_20200513_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiftdetail',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='shiftdetail',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='approved_shifts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shiftdetail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shifts', to=settings.AUTH_USER_MODEL),
        ),
    ]
