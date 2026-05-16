from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0022_remove_corevalue_description_ar_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="footer_about",
            field=models.TextField(
                blank=True,
                help_text="Short company description under the logo in the footer.",
                null=True,
                verbose_name="Footer — about the company",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="phone_landline",
            field=models.CharField(
                blank=True,
                help_text="Shown in the footer contact bar (e.g. +966…).",
                max_length=50,
                null=True,
                verbose_name="Landline phone",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="phone_mobile",
            field=models.CharField(
                blank=True,
                help_text="Shown in the footer contact bar (e.g. 05…).",
                max_length=50,
                null=True,
                verbose_name="Mobile phone",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="phone",
            field=models.CharField(
                blank=True,
                help_text="Legacy field. Prefer landline and mobile below.",
                max_length=120,
                null=True,
            ),
        ),
    ]
