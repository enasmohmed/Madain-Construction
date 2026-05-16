from django.db import migrations, models
from django.db.models import Q


def copy_block_image_to_panels(apps, schema_editor):
    Block = apps.get_model("pages", "MissionVisionValuesBlock")
    Panel = apps.get_model("pages", "MVVTabPanel")
    for block in Block.objects.exclude(side_image="").exclude(side_image=None):
        path = block.side_image.name
        if not path:
            continue
        for panel in Panel.objects.filter(block_id=block.pk).filter(
            Q(side_image="") | Q(side_image__isnull=True)
        ):
            panel.side_image = path
            panel.save(update_fields=["side_image"])


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0018_alter_mvvtabbullet_text_ar_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="mvvtabpanel",
            name="side_image",
            field=models.ImageField(
                blank=True,
                help_text="Large image beside the text for this tab (رؤيتنا / رسالتنا / قيمنا).",
                null=True,
                upload_to="mvv/tabs/",
                verbose_name="Tab side image",
            ),
        ),
        migrations.AlterField(
            model_name="missionvisionvaluesblock",
            name="side_image",
            field=models.ImageField(
                blank=True,
                help_text="Used only when a tab has no image of its own. Prefer uploading an image on each tab panel.",
                null=True,
                upload_to="mvv/",
                verbose_name="Default side image",
            ),
        ),
        migrations.RunPython(copy_block_image_to_panels, migrations.RunPython.noop),
    ]
