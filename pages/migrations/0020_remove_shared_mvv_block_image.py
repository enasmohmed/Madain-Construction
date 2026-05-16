from django.db import migrations, models

import pages.models


def move_block_image_to_tabs(apps, schema_editor):
    Block = apps.get_model("pages", "MissionVisionValuesBlock")
    Panel = apps.get_model("pages", "MVVTabPanel")
    for block in Block.objects.all():
        path = getattr(block, "side_image", "") or ""
        if not path:
            continue
        for panel in Panel.objects.filter(block_id=block.pk):
            if not panel.side_image:
                panel.side_image = path
                panel.save(update_fields=["side_image"])


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0019_mvvtabpanel_side_image"),
    ]

    operations = [
        migrations.RunPython(move_block_image_to_tabs, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="missionvisionvaluesblock",
            name="side_image",
        ),
        migrations.AlterField(
            model_name="mvvtabpanel",
            name="side_image",
            field=models.ImageField(
                blank=True,
                help_text="صورة هذا التبويب فقط — رؤيتنا / رسالتنا / قيمنا لكل واحد صورة منفصلة.",
                null=True,
                upload_to=pages.models.mvv_tab_side_image_upload_to,
                verbose_name="Side image for this tab only",
            ),
        ),
    ]
