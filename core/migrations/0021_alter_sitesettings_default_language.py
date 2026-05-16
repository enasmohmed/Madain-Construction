from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_sitesettings_our_work_section"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="default_language",
            field=models.CharField(
                choices=[("en", "English"), ("ar", "Arabic")],
                default="ar",
                max_length=5,
            ),
        ),
    ]
