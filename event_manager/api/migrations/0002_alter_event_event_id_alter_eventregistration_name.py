# Generated by Django 5.0.2 on 2024-02-20 19:42

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='eventregistration',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
