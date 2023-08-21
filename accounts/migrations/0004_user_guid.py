# Generated by Django 4.2.1 on 2023-08-21 11:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_user_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="guid",
            field=models.UUIDField(default=uuid.uuid1),
        ),
    ]
