# Generated by Django 4.2.21 on 2025-06-09 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "asynchronous_service_communication",
            "0002_decisioninstance_callback_url_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="decisioninstance",
            name="decision_taken_by",
            field=models.CharField(default="", max_length=20),
        ),
        migrations.AlterField(
            model_name="decisioninstance",
            name="decision",
            field=models.CharField(max_length=20),
        ),
    ]
