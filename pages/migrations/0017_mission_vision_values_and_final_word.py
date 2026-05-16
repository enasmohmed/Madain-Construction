import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0016_homeofferstrip"),
    ]

    operations = [
        migrations.CreateModel(
            name="MissionVisionValuesBlock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("side_image", models.ImageField(blank=True, null=True, upload_to="mvv/", verbose_name="Side image (large)")),
                (
                    "language",
                    models.CharField(
                        choices=[("en", "English"), ("ar", "Arabic")],
                        default="ar",
                        max_length=5,
                        verbose_name="Language row",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Visible")),
            ],
            options={
                "verbose_name": "Home — vision / mission / values",
                "verbose_name_plural": "Home — vision / mission / values",
            },
        ),
        migrations.CreateModel(
            name="MVVPartnerLogo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="mvv/logos/", verbose_name="Logo image")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Order")),
                ("alt_text", models.CharField(blank=True, max_length=200, verbose_name="Alt text")),
                ("alt_text_en", models.CharField(blank=True, max_length=200, null=True, verbose_name="Alt text")),
                ("alt_text_ar", models.CharField(blank=True, max_length=200, null=True, verbose_name="Alt text")),
                (
                    "block",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="partner_logos",
                        to="pages.missionvisionvaluesblock",
                        verbose_name="Block",
                    ),
                ),
            ],
            options={
                "verbose_name": "MVV — partner logo",
                "verbose_name_plural": "MVV — partner logos",
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="MVVTabPanel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "tab_key",
                    models.CharField(
                        choices=[("vision", "Vision"), ("mission", "Mission"), ("values", "Values")],
                        max_length=20,
                        verbose_name="Tab",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True,
                        help_text="e.g. رؤيتنا — shown on the pill button.",
                        max_length=120,
                        verbose_name="Tab label",
                    ),
                ),
                ("title_en", models.CharField(blank=True, help_text="e.g. رؤيتنا — shown on the pill button.", max_length=120, null=True, verbose_name="Tab label")),
                ("title_ar", models.CharField(blank=True, help_text="e.g. رؤيتنا — shown on the pill button.", max_length=120, null=True, verbose_name="Tab label")),
                ("body", ckeditor.fields.RichTextField(blank=True, null=True, verbose_name="Body text")),
                ("body_en", ckeditor.fields.RichTextField(blank=True, null=True, verbose_name="Body text")),
                ("body_ar", ckeditor.fields.RichTextField(blank=True, null=True, verbose_name="Body text")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="Tab order")),
                (
                    "block",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tab_panels",
                        to="pages.missionvisionvaluesblock",
                        verbose_name="Block",
                    ),
                ),
            ],
            options={
                "verbose_name": "MVV — tab panel",
                "verbose_name_plural": "MVV — tab panels",
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="MVVTabBullet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=400, verbose_name="Line text")),
                ("text_en", models.CharField(blank=True, max_length=400, null=True, verbose_name="Line text")),
                ("text_ar", models.CharField(blank=True, max_length=400, null=True, verbose_name="Line text")),
                (
                    "column",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Column 1"), (2, "Column 2")],
                        default=1,
                        verbose_name="Column",
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Order")),
                (
                    "panel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bullets",
                        to="pages.mvvtabpanel",
                        verbose_name="Tab panel",
                    ),
                ),
            ],
            options={
                "verbose_name": "MVV — list line",
                "verbose_name_plural": "MVV — list lines",
                "ordering": ["order", "id"],
            },
        ),
        migrations.AddConstraint(
            model_name="mvvtabpanel",
            constraint=models.UniqueConstraint(fields=("block", "tab_key"), name="pages_mvvtabpanel_unique_block_tab_key"),
        ),
        migrations.CreateModel(
            name="FinalWordSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(blank=True, max_length=200, verbose_name="Title")),
                ("title_en", models.CharField(blank=True, max_length=200, null=True, verbose_name="Title")),
                ("title_ar", models.CharField(blank=True, max_length=200, null=True, verbose_name="Title")),
                ("body", ckeditor.fields.RichTextField(blank=True, null=True, verbose_name="Body")),
                ("body_en", ckeditor.fields.RichTextField(blank=True, null=True, verbose_name="Body")),
                ("body_ar", ckeditor.fields.RichTextField(blank=True, null=True, verbose_name="Body")),
                ("image", models.ImageField(blank=True, null=True, upload_to="final_word/", verbose_name="Optional image")),
                (
                    "language",
                    models.CharField(
                        choices=[("en", "English"), ("ar", "Arabic")],
                        default="ar",
                        max_length=5,
                        verbose_name="Language row",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Visible")),
            ],
            options={
                "verbose_name": "Home — final word",
                "verbose_name_plural": "Home — final word",
            },
        ),
    ]
