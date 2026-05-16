from django.db import migrations


def seed_ar_services(apps, schema_editor):
    HomeServicesSection = apps.get_model("pages", "HomeServicesSection")
    HomeServiceCard = apps.get_model("pages", "HomeServiceCard")

    if HomeServicesSection.objects.filter(language="ar").exists():
        return

    section = HomeServicesSection.objects.create(
        title="خدماتنا",
        title_ar="خدماتنا",
        subtitle="",
        subtitle_ar="",
        footer_note=(
            "كل المشاريع يتم تنفيذها تحت إشراف مباشر من فريق هندسي وفني مؤهل "
            "لضمان مطابقة المواصفات وجودة التنفيذ."
        ),
        footer_note_ar=(
            "كل المشاريع يتم تنفيذها تحت إشراف مباشر من فريق هندسي وفني مؤهل "
            "لضمان مطابقة المواصفات وجودة التنفيذ."
        ),
        language="ar",
        is_active=True,
    )

    cards = [
        {
            "order": 0,
            "title": "أعمال الأساسات",
            "title_ar": "أعمال الأساسات",
            "points": (
                "تنفيذ الحفر والردم وتسوية الأرض.\n"
                "صب القواعد والأساسات المسلحة بجميع أنواعها.\n"
                "تنفيذ العزل المائي والحراري للأساسات.\n"
                "معالجة التربة وضمان استقرارها قبل البناء."
            ),
            "points_ar": (
                "تنفيذ الحفر والردم وتسوية الأرض.\n"
                "صب القواعد والأساسات المسلحة بجميع أنواعها.\n"
                "تنفيذ العزل المائي والحراري للأساسات.\n"
                "معالجة التربة وضمان استقرارها قبل البناء."
            ),
        },
        {
            "order": 1,
            "title": "أعمال الخرسانات",
            "title_ar": "أعمال الخرسانات",
            "points": (
                "تنفيذ الهياكل الخرسانية للمباني السكنية والتجارية والصناعية.\n"
                "صب الأعمدة والأسقف والجسور الخرسانية وفق أعلى معايير الجودة.\n"
                "استخدام مواد معتمدة وتقنيات حديثة لضمان المتانة والدقة."
            ),
            "points_ar": (
                "تنفيذ الهياكل الخرسانية للمباني السكنية والتجارية والصناعية.\n"
                "صب الأعمدة والأسقف والجسور الخرسانية وفق أعلى معايير الجودة.\n"
                "استخدام مواد معتمدة وتقنيات حديثة لضمان المتانة والدقة."
            ),
        },
        {
            "order": 2,
            "is_featured": True,
            "title": "أعمال التشطيبات الفاخرة",
            "title_ar": "أعمال التشطيبات الفاخرة",
            "intro": "تشطيبات داخلية وخارجية راقية تناسب مختلف الطرازات المعمارية.",
            "intro_ar": "تشطيبات داخلية وخارجية راقية تناسب مختلف الطرازات المعمارية.",
            "points": (
                "تنفيذ أعمال الدهانات والديكورات الجبسية والإضاءة.\n"
                "تركيب الأرضيات: الرخام، السيراميك، والباركيه بجودة عالية.\n"
                "تنفيذ تصاميم مخصصة تلائم ذوق العميل ومتطلبات المشروع."
            ),
            "points_ar": (
                "تنفيذ أعمال الدهانات والديكورات الجبسية والإضاءة.\n"
                "تركيب الأرضيات: الرخام، السيراميك، والباركيه بجودة عالية.\n"
                "تنفيذ تصاميم مخصصة تلائم ذوق العميل ومتطلبات المشروع."
            ),
        },
        {
            "order": 3,
            "title": "أعمال البنية التحتية",
            "title_ar": "أعمال البنية التحتية",
            "points": (
                "تنفيذ شبكات المياه والصرف الصحي وتصريف الأمطار.\n"
                "أعمال الكهرباء والاتصالات والتمديدات الأرضية.\n"
                "تنفيذ الطرق الداخلية والأرصفة والمواقف.\n"
                "التنسيق مع الجهات المختصة لضمان مطابقة المعايير والمواصفات."
            ),
            "points_ar": (
                "تنفيذ شبكات المياه والصرف الصحي وتصريف الأمطار.\n"
                "أعمال الكهرباء والاتصالات والتمديدات الأرضية.\n"
                "تنفيذ الطرق الداخلية والأرصفة والمواقف.\n"
                "التنسيق مع الجهات المختصة لضمان مطابقة المعايير والمواصفات."
            ),
        },
    ]

    for data in cards:
        featured = data.pop("is_featured", False)
        HomeServiceCard.objects.create(
            section=section,
            is_featured=featured,
            is_active=True,
            **data,
        )


def unseed(apps, schema_editor):
    HomeServicesSection = apps.get_model("pages", "HomeServicesSection")
    HomeServicesSection.objects.filter(language="ar", title="خدماتنا").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0025_home_services_points"),
    ]

    operations = [
        migrations.RunPython(seed_ar_services, unseed),
    ]
