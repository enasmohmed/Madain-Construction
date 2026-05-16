from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023_sitesettings_footer_phones_about"),
    ]

    operations = [
        migrations.AddField(
            model_name="footersection",
            name="instagram_url",
            field=models.URLField(blank=True, null=True, verbose_name="Instagram profile URL"),
        ),
        migrations.AddField(
            model_name="footersection",
            name="phone_landline",
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="Landline"),
        ),
        migrations.AddField(
            model_name="footersection",
            name="phone_mobile",
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="Mobile"),
        ),
        migrations.AddField(
            model_name="footersection",
            name="website",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="footersection",
            name="phone",
            field=models.CharField(
                blank=True,
                help_text="Legacy — use landline and mobile below.",
                max_length=120,
                null=True,
            ),
        ),
    ]
