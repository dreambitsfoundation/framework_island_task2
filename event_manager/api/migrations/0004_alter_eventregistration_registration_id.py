# Generated by Django 5.0.2 on 2024-02-20 21:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_eventregistration_name_alter_event_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregistration',
            name='registration_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
