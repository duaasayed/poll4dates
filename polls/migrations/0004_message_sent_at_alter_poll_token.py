# Generated by Django 4.2.1 on 2023-06-25 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0003_alter_poll_token_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="sent_at",
            field=models.DateTimeField(auto_now_add=True, default='1990-01-01'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="poll",
            name="token",
            field=models.CharField(default="hMNJ2a0n", max_length=8),
        ),
    ]
