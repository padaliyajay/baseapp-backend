# Generated by Django 3.2.16 on 2022-11-29 17:08

import django.utils.timezone
from django.db import migrations, models

import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SocialAuthAccessTokenCache",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("access_token", models.TextField()),
                ("oauth_token", models.TextField(blank=True)),
                ("oauth_verifier", models.TextField(blank=True)),
                ("code", models.TextField(blank=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
