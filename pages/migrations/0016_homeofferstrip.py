# Generated manually — modeltranslation columns for HomeOfferStrip

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0015_our_work_video_and_admin_en"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomeOfferStrip",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("column_1_title", models.CharField(blank=True, max_length=120, null=True, verbose_name="Column 1 — title")),
                ("column_1_title_en", models.CharField(blank=True, max_length=120, null=True, verbose_name="Column 1 — title")),
                ("column_1_title_ar", models.CharField(blank=True, max_length=120, null=True, verbose_name="Column 1 — title")),
                ("column_1_text", models.TextField(blank=True, null=True, verbose_name="Column 1 — text")),
                ("column_1_text_en", models.TextField(blank=True, null=True, verbose_name="Column 1 — text")),
                ("column_1_text_ar", models.TextField(blank=True, null=True, verbose_name="Column 1 — text")),
                ("column_2_title", models.CharField(blank=True, max_length=120, null=True, verbose_name="Column 2 — title")),
                ("column_2_title_en", models.CharField(blank=True, max_length=120, null=True, verbose_name="Column 2 — title")),
                ("column_2_title_ar", models.CharField(blank=True, max_length=120, null=True, verbose_name="Column 2 — title")),
                ("column_2_text", models.TextField(blank=True, null=True, verbose_name="Column 2 — text")),
                ("column_2_text_en", models.TextField(blank=True, null=True, verbose_name="Column 2 — text")),
                ("column_2_text_ar", models.TextField(blank=True, null=True, verbose_name="Column 2 — text")),
                ("column_3_title", models.CharField(blank=True, max_length=120, null=True, verbose_name="Column 3 — title")),
                ("column_3_title_en", models.CharField(blank=True, max_length=120, null=True, verbose_name="Column 3 — title")),
                ("column_3_title_ar", models.CharField(blank=True, max_length=120, null=True, verbose_name="Column 3 — title")),
                ("column_3_text", models.TextField(blank=True, null=True, verbose_name="Column 3 — text")),
                ("column_3_text_en", models.TextField(blank=True, null=True, verbose_name="Column 3 — text")),
                ("column_3_text_ar", models.TextField(blank=True, null=True, verbose_name="Column 3 — text")),
                (
                    "language",
                    models.CharField(
                        choices=[("en", "English"), ("ar", "Arabic")],
                        default="en",
                        max_length=5,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Home — offer strip (below hero)",
                "verbose_name_plural": "Home — offer strip (below hero)",
            },
        ),
    ]
