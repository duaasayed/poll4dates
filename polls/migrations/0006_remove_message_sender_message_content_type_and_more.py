# Generated by Django 4.2.1 on 2023-07-06 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("polls", "0005_alter_message_options_alter_poll_token"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="sender",
        ),
        migrations.AddField(
            model_name="message",
            name="content_type",
            field=models.ForeignKey(
                default=7,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="message",
            name="sender_id",
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="poll",
            name="token",
            field=models.CharField(default="hzXC8OPr", max_length=8),
        ),
    ]
