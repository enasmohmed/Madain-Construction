# Generated manually for modeltranslation (en/ar) fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_our_work_video_and_admin_en"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="our_work_section_title",
            field=models.CharField(
                blank=True,
                help_text="Home page «Our work» heading. Leave blank to use the default layout (OUR WORK / أعمالنا).",
                max_length=200,
                null=True,
                verbose_name="Our work — section title",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="our_work_section_title_ar",
            field=models.CharField(
                blank=True,
                help_text="Home page «Our work» heading. Leave blank to use the default layout (OUR WORK / أعمالنا).",
                max_length=200,
                null=True,
                verbose_name="Our work — section title",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="our_work_section_title_en",
            field=models.CharField(
                blank=True,
                help_text="Home page «Our work» heading. Leave blank to use the default layout (OUR WORK / أعمالنا).",
                max_length=200,
                null=True,
                verbose_name="Our work — section title",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="our_work_section_subtitle",
            field=models.CharField(
                blank=True,
                help_text="Short line under the heading. Leave blank for the default translated text.",
                max_length=400,
                null=True,
                verbose_name="Our work — section subtitle",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="our_work_section_subtitle_ar",
            field=models.CharField(
                blank=True,
                help_text="Short line under the heading. Leave blank for the default translated text.",
                max_length=400,
                null=True,
                verbose_name="Our work — section subtitle",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="our_work_section_subtitle_en",
            field=models.CharField(
                blank=True,
                help_text="Short line under the heading. Leave blank for the default translated text.",
                max_length=400,
                null=True,
                verbose_name="Our work — section subtitle",
            ),
        ),
    ]
