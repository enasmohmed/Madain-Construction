from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import SiteSettings, Sections, FooterSection


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'email', 'phone', 'default_language')
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'site_name',
                    'default_language',
                    'logo',
                    'preloader_logo',
                    'favicon',
                    'primary_color',
                    'secondary_color',
                ),
            },
        ),
        (
            _("Home — Our work"),
            {
                "fields": (
                    "our_work_section_title",
                    "our_work_section_subtitle",
                ),
            },
        ),
        (
            'Contact',
            {
                'fields': (
                    'phone_landline',
                    'phone_mobile',
                    'phone',
                    'working_hours',
                    'email',
                    'address',
                    'website',
                ),
            },
        ),
        (
            'Social',
            {'fields': ('facebook', 'linkedin', 'instagram', 'snapchat', 'tiktok')},
        ),
    )


@admin.register(Sections)
class SectionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'show_in_nav', 'is_visible')
    list_editable = ('order', 'show_in_nav', 'is_visible')


@admin.register(FooterSection)
class FooterSectionAdmin(admin.ModelAdmin):
    list_display = ("site_name", "email", "phone_landline", "phone_mobile", "is_active")
    fieldsets = (
        (
            _("Brand (footer only)"),
            {
                "fields": ("logo", "site_name", "description", "is_active"),
                "description": _(
                    "Logo and text here are shown only in the footer — not in the navbar."
                ),
            },
        ),
        (
            _("Contact bar (top of footer)"),
            {
                "fields": (
                    "phone_landline",
                    "phone_mobile",
                    "phone",
                    "email",
                    "map_url",
                    "address",
                    "website",
                ),
                "description": _(
                    "Landline + mobile appear in the footer bar with call links (tel:). "
                    "Map link opens from the globe icon and the address text."
                ),
            },
        ),
        (
            _("Quick links (footer column)"),
            {
                "fields": ("quick_links",),
                "description": _(
                    "JSON list, e.g. "
                    '[{"title": "من نحن", "url": "about"}, '
                    '{"title": "خدماتنا", "url": "services"}]. '
                    'Use "title" or "label". url: section slug (about, our-work, vision, mission, contact), '
                    "path, full URL, or Django URL name. Leave empty for built-in defaults."
                ),
            },
        ),
        (
            _("Social media (footer)"),
            {
                "fields": ("social_links", "instagram_url", "snapchat_url", "tiktok_url"),
                "description": _(
                    "Add social icons under the footer logo using JSON, or single URLs below. "
                    "If social_links is empty, Instagram/Snapchat URLs here or Site Settings → Social are used."
                ),
            },
        ),
        (
            _("Copyright"),
            {"fields": ("copyright_text",)},
        ),
    )
