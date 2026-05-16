from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    preloader_logo = models.ImageField(
        upload_to='settings/preloader/',
        blank=True,
        null=True,
        verbose_name=_("Preloader logo"),
        help_text=_(
            "Optional. Shown only on the loading screen (e.g. a light logo for a dark background). "
            "If empty, the main logo is used."
        ),
    )
    favicon = models.ImageField(upload_to='settings/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, blank=True, null=True)  # HEX
    secondary_color = models.CharField(max_length=7, blank=True, null=True)
    phone = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        help_text=_("Legacy field. Prefer landline and mobile below."),
    )
    phone_landline = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Landline phone"),
        help_text=_("Shown in the footer contact bar (e.g. +966…)."),
    )
    phone_mobile = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Mobile phone"),
        help_text=_("Shown in the footer contact bar (e.g. 05…)."),
    )
    footer_about = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Footer — about the company"),
        help_text=_("Short company description under the logo in the footer."),
    )
    working_hours = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=_("Shown in the header (e.g. ٧:٣٠ ص – ٩:٣٠ م)"),
    )
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    snapchat = models.URLField(blank=True, null=True, verbose_name=_("Snapchat profile URL"))
    tiktok = models.URLField(blank=True, null=True, verbose_name=_("TikTok profile URL"))
    website = models.URLField(blank=True, null=True)
    default_language = models.CharField(max_length=5, choices=[('en','English'), ('ar','Arabic')], default='ar')

    our_work_section_title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_("Our work — section title"),
        help_text=_("Home page «Our work» heading. Leave blank to use the default layout (OUR WORK / أعمالنا)."),
    )
    our_work_section_subtitle = models.CharField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name=_("Our work — section subtitle"),
        help_text=_("Short line under the heading. Leave blank for the default translated text."),
    )

    class Meta:
        verbose_name = _("Site Setting")
        verbose_name_plural = _("Site Settings")

    def __str__(self):
        return self.site_name or "Site Settings"



class FooterSection(models.Model):
    # شعار الموقع واسم الموقع
    logo = models.ImageField(upload_to='footer/', blank=True, null=True)
    site_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # ساعات العمل
    working_days = models.CharField(max_length=200, blank=True, null=True)
    working_dec = models.CharField(max_length=200, blank=True, null=True)
    working_hours = models.CharField(max_length=100, blank=True, null=True)
    working_off = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)

    # روابط سريعة — قائمة JSON: [{"label": "…", "url": "…"}, …]
    quick_links = models.JSONField(
        blank=True,
        null=True,
        help_text=_(
            'Example: [{"title": "من نحن", "url": "about"}, '
            '{"title": "خدماتنا", "url": "services"}]. '
            'Use "title" or "label". url: home section slug (about, services, our-work, vision, mission, contact) '
            'or Django name (contact_form) or path (/page/).'
        ),
    )

    # legacy — الخدمات تُعرض من تطبيق Services
    solutions = models.JSONField(blank=True, null=True)

    # روابط السوشيال — قائمة JSON في الفوتر (عمود «من نحن»)
    social_links = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("Social media links"),
        help_text=_(
            'Example: [{"platform": "snapchat", "url": "https://www.snapchat.com/add/yourpage"}, '
            '{"platform": "instagram", "url": "https://instagram.com/yourpage"}, '
            '{"platform": "x", "url": "https://x.com/yourpage"}]. '
            "platform: facebook, instagram, x (or twitter), youtube, snapchat, tiktok, linkedin, whatsapp. "
            "Leave empty to use Instagram URL below or Site Settings social fields."
        ),
    )

    # بيانات التواصل (مستقلة عن إعدادات الهيدر/النافبار)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        help_text=_("Legacy — use landline and mobile below."),
    )
    phone_landline = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Landline"))
    phone_mobile = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Mobile"))
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    map_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Map link"),
        help_text=_("Google Maps or map URL — used for the globe icon and address."),
    )
    instagram_url = models.URLField(blank=True, null=True, verbose_name=_("Instagram profile URL"))
    snapchat_url = models.URLField(blank=True, null=True, verbose_name=_("Snapchat profile URL"))
    tiktok_url = models.URLField(blank=True, null=True, verbose_name=_("TikTok profile URL"))

    # حقوق الملكية
    copyright_text = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Footer - {self.site_name}"



class Sections(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    is_visible = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    show_in_nav = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # نعتمد على العنوان الإنجليزي في الـ slug (أفضل تقنيًا)
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
