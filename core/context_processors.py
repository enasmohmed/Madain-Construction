import re

from django.core.cache import cache

from .footer_context import build_footer_data
from .models import FooterSection, SiteSettings, Sections

# تخزين مؤقت للقالب المشترك (رأس/تذييل) — يقلّل ضربات SQLite على أقراص بطيئة أثناء التطوير
_SITE_CONTEXT_CACHE_KEY = "core:site_settings_context:v18"
_SITE_CONTEXT_CACHE_TTL = 45


def _header_phones_from_site(site):
    """Landline + mobile for the top bar (split legacy combined phone if needed)."""
    if not site:
        return "", ""
    landline = (site.phone_landline or "").strip()
    mobile = (site.phone_mobile or "").strip()
    if landline or mobile:
        return landline, mobile
    raw = (site.phone or "").strip()
    if not raw:
        return "", ""
    parts = [p.strip() for p in raw.split("|") if p.strip()]
    if len(parts) >= 2:
        return parts[0], parts[1]
    return parts[0], ""


def _whatsapp_from_site(site, phone_mobile="", phone_landline=""):
    """رابط wa.me + الرقم للعرض (يفضّل الجوال)."""
    raw = (phone_mobile or phone_landline or "").strip()
    if not raw and site:
        raw = (site.phone_mobile or site.phone_landline or site.phone or "").strip()
        if "|" in raw:
            parts = [p.strip() for p in raw.split("|") if p.strip()]
            raw = parts[-1] if parts else raw
    if not raw:
        return "", ""

    digits = re.sub(r"\D", "", raw)
    if not digits:
        return "", ""

    if digits.startswith("00"):
        digits = digits[2:]
    elif digits.startswith("0") and len(digits) >= 9:
        digits = "966" + digits[1:]
    elif not digits.startswith("966") and len(digits) <= 10:
        digits = "966" + digits.lstrip("0")

    return f"https://wa.me/{digits}", raw


def site_settings_context(request):
    # لوحة الإدارة لا تحتاج إعدادات الموقع — تجاهلها يقلّل الاستعلامات ويُسرّع Jazzmin/الأدمن
    path = getattr(request, "path", "") or ""
    if path.startswith("/admin"):
        return {}

    cached = cache.get(_SITE_CONTEXT_CACHE_KEY)
    if cached is not None:
        return cached

    site = SiteSettings.objects.first()
    lang = getattr(request, "LANGUAGE_CODE", None) or "ar"
    phone_landline, phone_mobile = _header_phones_from_site(site)
    whatsapp_url, whatsapp_number = _whatsapp_from_site(
        site, phone_mobile=phone_mobile, phone_landline=phone_landline
    )

    data = {
        'site_name': site.site_name if site else '',
        'primary_color': site.primary_color if site else '#ffa610',
        'secondary_color': site.secondary_color if site else '#E6E6E6',
        'website': site.website if site else '',
        'phone': site.phone if site else '',
        'phone_landline': phone_landline,
        'phone_mobile': phone_mobile,
        'whatsapp_url': whatsapp_url,
        'whatsapp_number': whatsapp_number,
        'working_hours': site.working_hours if site else '',
        'email': site.email if site else '',
        'address': site.address if site else '',
        'facebook': site.facebook if site else '',
        'linkedin': site.linkedin if site else '',
        'instagram': site.instagram if site else '',
        'snapchat': site.snapchat if site else '',
        'tiktok': site.tiktok if site else '',

        'our_work_section_title': (site.our_work_section_title if site else '') or '',
        'our_work_section_subtitle': (site.our_work_section_subtitle if site else '') or '',

        'logo_url': (
            site.logo.url
            if site and site.logo
            else '/static/images/demo-site-logo.png'
        ),

        'preloader_logo_url': (
            site.preloader_logo.url
            if site and site.preloader_logo
            else (
                site.logo.url
                if site and site.logo
                else '/static/images/demo-site-logo.png'
            )
        ),

        'favicon_url': (
            site.favicon.url
            if site and site.favicon
            else '/static/images/demo-favicon.png'
        ),
    }

    nav_sections = Sections.objects.filter(
        is_visible=True,
        show_in_nav=True,
    ).order_by('order')

    footer_section = FooterSection.objects.filter(is_active=True).first()
    footer_data = build_footer_data(
        footer_section,
        site={
            "facebook": data.get("facebook"),
            "instagram": data.get("instagram"),
            "linkedin": data.get("linkedin"),
            "snapchat": data.get("snapchat"),
            "tiktok": data.get("tiktok"),
        },
    )

    footer_our_work = []
    try:
        from pages.models import OurWorkImage

        for item in OurWorkImage.objects.filter(is_active=True).order_by("order", "id"):
            if not item.image:
                continue
            footer_our_work.append(
                {
                    "image_url": item.image.url,
                    "alt": "",
                }
            )
            if len(footer_our_work) >= 6:
                break
    except Exception:
        footer_our_work = []

    result = {
        'site_settings': data,
        'logo_url': data['logo_url'],
        'favicon_url': data['favicon_url'],
        'nav_sections': nav_sections,
        'footer_data': footer_data,
        'footer_our_work': footer_our_work,
    }
    cache.set(_SITE_CONTEXT_CACHE_KEY, result, _SITE_CONTEXT_CACHE_TTL)
    return result
