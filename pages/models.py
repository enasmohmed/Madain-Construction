import os

from django.core.exceptions import ValidationError
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _


def mvv_tab_side_image_upload_to(instance, filename):
    """صورة مستقلة لكل تبويب: mvv/tabs/vision/ … mission/ … values/"""
    tab = (instance.tab_key or "other").strip() or "other"
    base, ext = os.path.splitext(filename)
    safe = f"{base}{ext}" if ext else filename
    return f"mvv/tabs/{tab}/{safe}"

# Create your models here.






class HeroSlide(models.Model):
    """شرائح السلايدر في الصفحة الرئيسية — تُدار من الإدارة."""
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    tagline = models.CharField(max_length=200, blank=True, verbose_name=_("Subtitle (small line / h4)"))
    heading = models.CharField(max_length=255, blank=True, verbose_name=_("Main heading (h1)"))
    lead = models.TextField(blank=True, verbose_name=_("Paragraph text"))
    background_image = models.ImageField(upload_to="hero/slides/", blank=True, null=True)
    foreground_image = models.ImageField(
        upload_to="hero/slides/",
        blank=True,
        null=True,
        verbose_name=_("Front image (optional)"),
    )
    button_text = models.CharField(max_length=80, blank=True)
    button_link = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Example: /contact/ or full URL. Leave empty to use contact page."),
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Hero slide")
        verbose_name_plural = _("Hero slides")

    def __str__(self):
        if self.heading:
            return self.heading[:80]
        return f"Hero slide #{self.pk}"


class HeroSlideBackgroundImage(models.Model):
    """صور خلفية إضافية لنفس شريحة الهيرو — كل صورة تظهر كشريحة منفصلة في Owl بنفس النص والزر."""

    slide = models.ForeignKey(
        HeroSlide,
        on_delete=models.CASCADE,
        related_name="extra_backgrounds",
        verbose_name=_("Hero slide"),
    )
    image = models.ImageField(upload_to="hero/slides/bg/", verbose_name=_("Background image"))
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Hero slide extra background")
        verbose_name_plural = _("Hero slide extra backgrounds")

    def __str__(self):
        return f"{self.slide_id} — {self.image.name}"


class HeroBannerSettings(models.Model):
    """إعداد واحد (صف واحد): فيديو خلفية بدل سلايدر الصور أو العكس."""

    prefer_video = models.BooleanField(
        default=False,
        verbose_name=_("Use video instead of image slider"),
        help_text=_("When enabled, shows one looping muted video; image carousel is hidden."),
    )
    background_video = models.FileField(
        upload_to="hero/video/",
        blank=True,
        null=True,
        verbose_name=_("Background video file"),
        help_text=_("MP4 or WebM. Plays muted, looped, autoplay."),
    )
    external_video_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name=_("Video URL (optional)"),
        help_text=_("Direct link to an MP4/WebM file. If set, overrides the uploaded file."),
    )

    class Meta:
        verbose_name = _("Hero banner")
        verbose_name_plural = _("Hero banner")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return str(_("Hero banner"))


class HeroOverlayImage(models.Model):
    """صور إضافية أسفل الهيرو (فيديو أو سلايدر) — غالبًا الشكل الزخرفي السفلي."""

    banner = models.ForeignKey(
        HeroBannerSettings,
        on_delete=models.CASCADE,
        related_name="overlay_images",
    )
    image = models.ImageField(upload_to="hero/overlay/")
    order = models.PositiveIntegerField(default=0)
    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Hero bottom image")
        verbose_name_plural = _("Hero bottom images")

    def __str__(self):
        return f"{self.alt_text or self.image.name} (#{self.pk})"


class OurWorkImage(models.Model):
    """Home «Our work» gallery tile: upload either an image or a video (not both)."""

    image = models.ImageField(
        upload_to="our_work/",
        blank=True,
        null=True,
        verbose_name=_("Image"),
        help_text=_("Use this or video — not both."),
    )
    video = models.FileField(
        upload_to="our_work/video/",
        blank=True,
        null=True,
        verbose_name=_("Video"),
        help_text=_("MP4 or WebM. Use this or image — not both."),
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Display order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Our work item")
        verbose_name_plural = _("Our work items")

    def clean(self):
        super().clean()
        has_image = bool(self.image)
        has_video = bool(self.video)
        if not has_image and not has_video:
            raise ValidationError(_("Please add either an image or a video."))
        if has_image and has_video:
            raise ValidationError(_("Please use only one: image or video."))

    def save(
        self,
        *,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        # Django 6+: Model.save() is keyword-only — do not use *args/**kwargs forwarding.
        self.full_clean()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def __str__(self):
        kind = "video" if self.video else "image"
        return f"Our work item #{self.pk} ({kind})"


class HomeOfferStrip(models.Model):
    """
    Three columns + wide image under the hero (Simply «offer» strip).
    Icons and the bottom illustration are static files in the template.
    """

    column_1_title = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name=_("Column 1 — title"),
    )
    column_1_text = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Column 1 — text"),
    )
    column_2_title = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name=_("Column 2 — title"),
    )
    column_2_text = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Column 2 — text"),
    )
    column_3_title = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name=_("Column 3 — title"),
    )
    column_3_text = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Column 3 — text"),
    )
    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("ar", "Arabic")],
        default="en",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Home — offer strip (below hero)")
        verbose_name_plural = _("Home — offer strip (below hero)")

    def __str__(self):
        for t in (self.column_1_title, self.column_2_title, self.column_3_title):
            if t and str(t).strip():
                return str(t).strip()[:80]
        return str(_("Home offer strip"))


class HomeServicesSection(models.Model):
    """خدماتنا — أربع كروت فوق معرض الأعمال."""

    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Section title"),
        help_text=_('Example: "Our services" / «خدماتنا»'),
    )
    subtitle = models.TextField(
        blank=True,
        verbose_name=_("Intro text (under title)"),
    )
    footer_note = models.TextField(
        blank=True,
        verbose_name=_("Closing note (below cards)"),
        help_text=_(
            "Optional paragraph shown under all four service cards "
            "(e.g. supervision by engineering team)."
        ),
    )
    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("ar", "Arabic")],
        default="ar",
        verbose_name=_("Language row"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        verbose_name = _("Home — our services (4 cards)")
        verbose_name_plural = _("Home — our services (4 cards)")

    def __str__(self):
        t = (self.title or "").strip()
        return t[:80] if t else str(_("Our services section"))


class HomeServiceCard(models.Model):
    section = models.ForeignKey(
        HomeServicesSection,
        on_delete=models.CASCADE,
        related_name="cards",
        verbose_name=_("Section"),
    )
    title = models.CharField(
        max_length=160,
        blank=True,
        verbose_name=_("Service name"),
        help_text=_('Example: «Foundation works» / «أعمال الأساسات».'),
    )
    intro = models.TextField(
        blank=True,
        verbose_name=_("Short intro (optional)"),
        help_text=_("One line before the bullet list, if needed."),
    )
    points = models.TextField(
        blank=True,
        verbose_name=_("Bullet points"),
        help_text=_("One service point per line (each line becomes a bullet)."),
    )
    icon = models.ImageField(
        upload_to="services/icons/",
        blank=True,
        null=True,
        verbose_name=_("Icon (optional)"),
        help_text=_("Bottom corner icon. If empty, a default icon is used."),
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("Highlighted card"),
        help_text=_("Orange style by default (like the center card in the theme)."),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Service item")
        verbose_name_plural = _("Service items")

    def __str__(self):
        if self.title and str(self.title).strip():
            return str(self.title).strip()[:80]
        return f"{_('Service')} #{self.pk or '?'}"

    @property
    def bullet_lines(self):
        if not self.points:
            return []
        return [line.strip() for line in str(self.points).splitlines() if line.strip()]


class MissionVisionValuesBlock(models.Model):
    """
    Home split block: dark panel with tabs (رؤيتنا / رسالتنا / قيمنا).
    كل تبويب له صورته في MVVTabPanel.side_image.
    """

    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("ar", "Arabic")],
        default="ar",
        verbose_name=_("Language row"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        verbose_name = _("Home — vision / mission / values")
        verbose_name_plural = _("Home — vision / mission / values")

    def __str__(self):
        return f"MVV — {self.get_language_display()}"


class MVVPartnerLogo(models.Model):
    block = models.ForeignKey(
        MissionVisionValuesBlock,
        on_delete=models.CASCADE,
        related_name="partner_logos",
        verbose_name=_("Block"),
    )
    image = models.ImageField(upload_to="mvv/logos/", verbose_name=_("Logo image"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))
    alt_text = models.CharField(max_length=200, blank=True, verbose_name=_("Alt text"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("MVV — partner logo")
        verbose_name_plural = _("MVV — partner logos")

    def __str__(self):
        return f"Logo #{self.pk} ({self.block_id})"


class MVVTabPanel(models.Model):
    class TabKey(models.TextChoices):
        VISION = "vision", _("Vision")
        MISSION = "mission", _("Mission")
        VALUES = "values", _("Values")

    block = models.ForeignKey(
        MissionVisionValuesBlock,
        on_delete=models.CASCADE,
        related_name="tab_panels",
        verbose_name=_("Block"),
    )
    tab_key = models.CharField(
        max_length=20,
        choices=TabKey.choices,
        verbose_name=_("Tab"),
    )
    title = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_("Tab label"),
        help_text=_("e.g. رؤيتنا — shown on the pill button."),
    )
    body = RichTextField(blank=True, null=True, verbose_name=_("Body text"))
    side_image = models.ImageField(
        upload_to=mvv_tab_side_image_upload_to,
        blank=True,
        null=True,
        verbose_name=_("Side image for this tab only"),
        help_text=_(
            "صورة هذا التبويب فقط — رؤيتنا / رسالتنا / قيمنا لكل واحد صورة منفصلة."
        ),
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("Tab order"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("MVV — tab panel")
        verbose_name_plural = _("MVV — tab panels")
        constraints = [
            models.UniqueConstraint(
                fields=["block", "tab_key"],
                name="pages_mvvtabpanel_unique_block_tab_key",
            )
        ]

    def __str__(self):
        return f"{self.get_tab_key_display()} ({self.block_id})"


class MVVTabBullet(models.Model):
    panel = models.ForeignKey(
        MVVTabPanel,
        on_delete=models.CASCADE,
        related_name="bullets",
        verbose_name=_("Tab panel"),
    )
    text = models.CharField(max_length=400, verbose_name=_("Line text"))
    column = models.PositiveSmallIntegerField(
        choices=[(1, _("Column 1")), (2, _("Column 2"))],
        default=1,
        verbose_name=_("Column"),
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("MVV — list line")
        verbose_name_plural = _("MVV — list lines")

    def __str__(self):
        return self.text[:60]


class FinalWordColumnLine(models.Model):
    """سطر نص داخل «كلمة أخيرة» — عمود 1 أو 2 يظهران جنب بعض على الموقع."""

    section = models.ForeignKey(
        "FinalWordSection",
        on_delete=models.CASCADE,
        related_name="column_lines",
        verbose_name=_("Section"),
    )
    text = models.CharField(max_length=500, verbose_name=_("Line text"))
    column = models.PositiveSmallIntegerField(
        choices=[(1, _("Column 1")), (2, _("Column 2"))],
        default=1,
        verbose_name=_("Column"),
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Final word — column line")
        verbose_name_plural = _("Final word — column lines")

    def __str__(self):
        return self.text[:60]


class FinalWordSection(models.Model):
    """كلمة أخيرة — block before contact / newsletter."""

    title = models.CharField(max_length=200, blank=True, verbose_name=_("Title"))
    body = RichTextField(
        blank=True,
        null=True,
        verbose_name=_("Body (legacy)"),
        help_text=_(
            "Optional. Prefer «Final word — column lines» below for two side-by-side columns."
        ),
    )
    image = models.ImageField(
        upload_to="final_word/",
        blank=True,
        null=True,
        verbose_name=_("Side image (optional)"),
        help_text=_(
            "Leave empty: two text columns use the full width. "
            "Upload a file: image appears beside the text (50/50)."
        ),
    )
    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("ar", "Arabic")],
        default="ar",
        verbose_name=_("Language row"),
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Visible"))

    class Meta:
        verbose_name = _("Home — final word")
        verbose_name_plural = _("Home — final word")

    def __str__(self):
        t = (self.title or "").strip()
        return t[:80] if t else f"Final word — {self.get_language_display()}"

    def lines_for_column(self, column):
        return self.column_lines.filter(column=column)

    @property
    def col1_lines(self):
        return self.lines_for_column(1)

    @property
    def col2_lines(self):
        return self.lines_for_column(2)