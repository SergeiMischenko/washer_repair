# Generated by Django 5.0.6 on 2024-06-06 15:01

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0005_alter_repairrequest_options_alter_review_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="repairrequest",
            name="token",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
