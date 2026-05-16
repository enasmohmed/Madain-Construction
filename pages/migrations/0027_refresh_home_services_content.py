"""Ensure Arabic service cards have bullet points (idempotent)."""

from django.db import migrations

CARDS = [
    {
        "order": 0,
        "title": "أعمال الأساسات",
        "points": (
            "تنفيذ الحفر والردم وتسوية الأرض.\n"
            "صب القواعد والأساسات المسلحة بجميع أنواعها.\n"
            "تنفيذ العزل المائي والحراري للأساسات.\n"
            "معالجة التربة وضمان استقرارها قبل البناء."
        ),
    },
    {
        "order": 1,
        "title": "أعمال الخرسانات",
        "points": (
            "تنفيذ الهياكل الخرسانية للمباني السكنية والتجارية والصناعية.\n"
            "صب الأعمدة والأسقف والجسور الخرسانية وفق أعلى معايير الجودة.\n"
            "استخدام مواد معتمدة وتقنيات حديثة لضمان المتانة والدقة."
        ),
    },
    {
        "order": 2,
        "title": "أعمال التشطيبات الفاخرة",
        "intro": "تشطيبات داخلية وخارجية راقية تناسب مختلف الطرازات المعمارية.",
        "is_featured": True,
        "points": (
            "تنفيذ أعمال الدهانات والديكورات الجبسية والإضاءة.\n"
            "تركيب الأرضيات: الرخام، السيراميك، والباركيه بجودة عالية.\n"
            "تنفيذ تصاميم مخصصة تلائم ذوق العميل ومتطلبات المشروع."
        ),
    },
    {
        "order": 3,
        "title": "أعمال البنية التحتية",
        "points": (
            "تنفيذ شبكات المياه والصرف الصحي وتصريف الأمطار.\n"
            "أعمال الكهرباء والاتصالات والتمديدات الأرضية.\n"
            "تنفيذ الطرق الداخلية والأرصفة والمواقف.\n"
            "التنسيق مع الجهات المختصة لضمان مطابقة المعايير والمواصفات."
        ),
    },
]

FOOTER = (
    "كل المشاريع يتم تنفيذها تحت إشراف مباشر من فريق هندسي وفني مؤهل "
    "لضمان مطابقة المواصفات وجودة التنفيذ."
)


def refresh(apps, schema_editor):
    HomeServicesSection = apps.get_model("pages", "HomeServicesSection")
    HomeServiceCard = apps.get_model("pages", "HomeServiceCard")

    section, _ = HomeServicesSection.objects.get_or_create(
        language="ar",
        defaults={
            "title": "خدماتنا",
            "title_ar": "خدماتنا",
            "is_active": True,
        },
    )
    if not section.title:
        section.title = "خدماتنا"
        section.title_ar = "خدماتنا"
    if not section.footer_note:
        section.footer_note = FOOTER
        section.footer_note_ar = FOOTER
    section.is_active = True
    section.save()

    for data in CARDS:
        featured = data.pop("is_featured", False)
        intro = data.pop("intro", "")
        card, created = HomeServiceCard.objects.get_or_create(
            section=section,
            order=data["order"],
            defaults={
                "title": data["title"],
                "title_ar": data["title"],
                "points": data["points"],
                "points_ar": data["points"],
                "intro": intro,
                "intro_ar": intro,
                "is_featured": featured,
                "is_active": True,
            },
        )
        if created:
            continue
        updated = False
        if not (card.points or "").strip():
            card.points = data["points"]
            card.points_ar = data["points"]
            updated = True
        if not (card.title or "").strip():
            card.title = data["title"]
            card.title_ar = data["title"]
            updated = True
        if intro and not (card.intro or "").strip():
            card.intro = intro
            card.intro_ar = intro
            updated = True
        if featured:
            card.is_featured = True
            updated = True
        card.is_active = True
        if updated:
            card.save()


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0026_seed_home_services_ar"),
    ]

    operations = [
        migrations.RunPython(refresh, migrations.RunPython.noop),
    ]
