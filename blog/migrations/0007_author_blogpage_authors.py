# Generated by Django 5.0.2 on 2024-03-28 06:24

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_blogpagegalleryimage"),
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
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
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "author_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Authors",
            },
        ),
        migrations.AddField(
            model_name="blogpage",
            name="authors",
            field=modelcluster.fields.ParentalManyToManyField(
                blank=True, null=True, to="blog.author"
            ),
        ),
    ]