from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline, TranslationTabularInline

import pages.translation  # noqa: F401 — قبل TranslationAdmin (تسجيل HeroSlide وغيره)

from .models import (
    HeroSlide,
    HeroSlideBackgroundImage,
    HeroBannerSettings,
    HeroOverlayImage,
    OurWorkImage,
    HomeOfferStrip,
    HomeServicesSection,
    HomeServiceCard,
    MissionVisionValuesBlock,
    MVVPartnerLogo,
    MVVTabPanel,
    MVVTabBullet,
    FinalWordSection,
    FinalWordColumnLine,
)

class HeroOverlayImageInline(admin.TabularInline):
    model = HeroOverlayImage
    extra = 0
    ordering = ("order",)


@admin.register(HeroBannerSettings)
class HeroBannerSettingsAdmin(admin.ModelAdmin):
    """صف واحد فقط — إعداد فيديو الهيرو مقابل السلايدر."""

    inlines = (HeroOverlayImageInline,)

    def has_add_permission(self, request):
        return not HeroBannerSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class HeroSlideBackgroundImageInline(admin.TabularInline):
    model = HeroSlideBackgroundImage
    extra = 0
    ordering = ("order",)


@admin.register(HeroSlide)
class HeroSlideAdmin(TranslationAdmin):
    list_display = ('heading', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('heading',)
    list_filter = ('is_active',)
    ordering = ('order', 'id')
    inlines = (HeroSlideBackgroundImageInline,)


class HomeServiceCardInline(TranslationStackedInline):
    model = HomeServiceCard
    extra = 1
    max_num = 4
    ordering = ("order", "id")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "intro",
                    "points",
                    "icon",
                    "order",
                    "is_featured",
                    "is_active",
                ),
                "description": _(
                    "«Points»: enter one bullet per line. "
                    "Example: «Excavation and backfill» on its own line."
                ),
            },
        ),
    )


@admin.register(HomeServicesSection)
class HomeServicesSectionAdmin(TranslationAdmin):
    list_display = ("title", "language", "is_active", "card_count")
    list_filter = ("is_active", "language")
    inlines = (HomeServiceCardInline,)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "subtitle",
                    "footer_note",
                    "language",
                    "is_active",
                ),
            },
        ),
    )

    @admin.display(description=_("Cards"))
    def card_count(self, obj):
        return obj.cards.filter(is_active=True).count()


@admin.register(HomeOfferStrip)
class HomeOfferStripAdmin(admin.ModelAdmin):
    list_display = ("column_1_title", "language", "is_active")
    list_filter = ("is_active", "language")
    fieldsets = (
        (_("Column 1"), {"fields": ("column_1_title", "column_1_text")}),
        (_("Column 2"), {"fields": ("column_2_title", "column_2_text")}),
        (_("Column 3"), {"fields": ("column_3_title", "column_3_text")}),
        (_("Visibility"), {"fields": ("language", "is_active")}),
    )


@admin.register(OurWorkImage)
class OurWorkImageAdmin(admin.ModelAdmin):
    # `thumb` first + list_display_links: required when using list_editable (Django admin rules).
    list_display = ("thumb", "order", "media_kind", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("thumb",)
    list_filter = ("is_active",)
    list_per_page = 50
    ordering = ("order", "id")

    @admin.display(description="Preview")
    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" alt="" width="56" height="56" style="object-fit:cover;border-radius:4px"/>',
                obj.image.url,
            )
        if obj.video:
            return format_html(
                '<span style="display:inline-block;padding:6px 10px;background:#1e293b;color:#f8fafc;'
                'border-radius:4px;font-size:11px;font-weight:600;">{}</span>',
                "VIDEO",
            )
        return "—"

    @admin.display(description="Type")
    def media_kind(self, obj):
        if obj.video:
            return "Video"
        if obj.image:
            return "Image"
        return "—"


class _MVVTabularInlineAdminMixin:
    class Media:
        css = {"all": ("admin/css/mvv_inlines.css",)}


class MVVPartnerLogoInline(_MVVTabularInlineAdminMixin, TranslationTabularInline):
    model = MVVPartnerLogo
    extra = 0
    ordering = ("order",)


class MVVTabPanelInline(TranslationStackedInline):
    """رؤيتنا + رسالتنا + قيمنا — كل تبويب بصورة ونص مستقلين."""

    model = MVVTabPanel
    extra = 0
    min_num = 3
    max_num = 3
    can_delete = False
    ordering = ("order",)
    readonly_fields = ("tab_key", "tab_label_ar")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "tab_key",
                    "tab_label_ar",
                    "side_image",
                    "title",
                ),
            },
        ),
        (_("Tab text"), {"fields": ("body",)}),
    )

    @admin.display(description=_("Tab"))
    def tab_label_ar(self, obj):
        labels = {
            "vision": "رؤيتنا",
            "mission": "رسالتنا",
            "values": "قيمنا",
        }
        return labels.get(obj.tab_key, obj.get_tab_key_display())


@admin.register(MissionVisionValuesBlock)
class MissionVisionValuesBlockAdmin(admin.ModelAdmin):
    list_display = ("language", "is_active", "id")
    list_filter = ("is_active", "language")
    fieldsets = ((None, {"fields": ("language", "is_active")}),)
    inlines = (MVVTabPanelInline, MVVPartnerLogoInline)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        for key, order in (("vision", 0), ("mission", 1), ("values", 2)):
            MVVTabPanel.objects.get_or_create(
                block=obj,
                tab_key=key,
                defaults={"order": order},
            )


class MVVTabBulletInline(_MVVTabularInlineAdminMixin, TranslationTabularInline):
    model = MVVTabBullet
    extra = 1
    ordering = ("order", "id")
    fields = ("text", "column", "order")


@admin.register(MVVTabPanel)
class MVVTabPanelAdmin(_MVVTabularInlineAdminMixin, TranslationAdmin):
    """تعديل النقاط (bullets) — الصورة والنص الأساسي من صفحة Home — vision / mission / values."""

    list_display = ("block", "tab_key", "title", "side_image_thumb", "order")
    list_filter = ("tab_key", "block")
    list_editable = ("order",)
    list_display_links = ("tab_key",)
    ordering = ("block", "order", "id")
    raw_id_fields = ("block",)
    inlines = (MVVTabBulletInline,)
    fieldsets = (
        (
            _("This tab only"),
            {
                "fields": ("block", "tab_key", "title", "order", "side_image"),
                "description": _(
                    "Each tab (vision / mission / values) has its own image file. "
                    "Upload a different image for each tab — they are not shared."
                ),
            },
        ),
        (_("Tab text"), {"fields": ("body",)}),
    )

    @admin.display(description=_("Image"))
    def side_image_thumb(self, obj):
        if not obj.side_image:
            return "—"
        return format_html(
            '<img src="{}" alt="" width="72" height="48" style="object-fit:cover;border-radius:4px"/>',
            obj.side_image.url,
        )


class FinalWordColumnLineInline(_MVVTabularInlineAdminMixin, TranslationTabularInline):
    model = FinalWordColumnLine
    extra = 1
    ordering = ("order", "id")
    fields = ("text", "column", "order")


@admin.register(FinalWordSection)
class FinalWordSectionAdmin(_MVVTabularInlineAdminMixin, TranslationAdmin):
    list_display = ("title", "language", "is_active")
    list_filter = ("is_active", "language")
    inlines = (FinalWordColumnLineInline,)
    fieldsets = (
        (None, {"fields": ("title", "language", "is_active")}),
        (
            _("Image (optional)"),
            {
                "fields": ("image",),
                "description": _(
                    "Leave empty to show only two text columns (Column 1 + Column 2) at full width. "
                    "Upload an image to show it on the side next to the text."
                ),
            },
        ),
        (
            _("Body (optional)"),
            {
                "fields": ("body",),
                "classes": ("collapse",),
                "description": _(
                    "Use «Final word — column lines» at the bottom: pick Column 1 or Column 2 "
                    "so text appears in two side-by-side columns on the home page."
                ),
            },
        ),
    )
