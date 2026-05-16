from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0024_footersection_contact_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="footersection",
            name="map_url",
            field=models.URLField(
                blank=True,
                help_text="Google Maps or map URL — used for the globe icon and address.",
                null=True,
                verbose_name="Map link",
            ),
        ),
    ]
