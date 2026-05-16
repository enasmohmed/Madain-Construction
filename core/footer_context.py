from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext_lazy as _

from core.home_anchors import anchor_for_slug

_SOCIAL_PLATFORM_META = {
    "facebook": {"icon": "fa-facebook", "label": "Facebook", "modifier": "facebook"},
    "instagram": {"icon": "fa-instagram", "label": "Instagram", "modifier": "instagram"},
    "twitter": {"icon": "fa-twitter", "label": "X", "modifier": "x"},
    "x": {"icon": "fa-twitter", "label": "X", "modifier": "x"},
    "youtube": {"icon": "fa-youtube-play", "label": "YouTube", "modifier": "youtube"},
    "snapchat": {"icon": "fa-snapchat-ghost", "label": "Snapchat", "modifier": "snapchat"},
    "linkedin": {"icon": "fa-linkedin", "label": "LinkedIn", "modifier": "linkedin"},
    "whatsapp": {"icon": "fa-whatsapp", "label": "WhatsApp", "modifier": "whatsapp"},
    "tiktok": {"icon": "", "label": "TikTok", "modifier": "tiktok", "icon_type": "svg"},
}


def _normalize_social_platform(raw):
    key = (raw or "").strip().lower()
    aliases = {
        "fb": "facebook",
        "ig": "instagram",
        "yt": "youtube",
        "sc": "snapchat",
        "snap": "snapchat",
        "سناب": "snapchat",
        "سنابشات": "snapchat",
        "wa": "whatsapp",
        "tt": "tiktok",
        "tiktok": "tiktok",
        "تيك توك": "tiktok",
        "تيكتوك": "tiktok",
    }
    return aliases.get(key, key)


def _social_item(platform, url, custom_label=""):
    platform_key = _normalize_social_platform(platform)
    meta = _SOCIAL_PLATFORM_META.get(
        platform_key,
        {
            "icon": "fa-share-alt",
            "label": custom_label or platform_key.title(),
            "modifier": "generic",
        },
    )
    label = (custom_label or meta["label"]).strip()
    href = (url or "").strip()
    if not href or href == "#":
        return None
    if not href.startswith(("http://", "https://", "mailto:", "tel:")):
        href = f"https://{href.lstrip('/')}"
    return {
        "platform": platform_key,
        "href": href,
        "icon": meta["icon"],
        "label": label,
        "modifier": meta["modifier"],
        "icon_type": meta.get("icon_type", "fa"),
    }


def _social_platforms_in(items):
    return {item.get("platform") for item in items}


def _append_social_if_missing(items, platform, url, custom_label=""):
    if platform in _social_platforms_in(items):
        return
    item = _social_item(platform, url, custom_label)
    if item:
        items.append(item)


def _parse_social_links(section, site=None):
    items = []

    if section and isinstance(section.social_links, list):
        for entry in section.social_links:
            if not isinstance(entry, dict):
                continue
            custom_label = (entry.get("label") or entry.get("title") or "").strip()
            platform = entry.get("platform") or entry.get("network") or entry.get("icon")
            url = entry.get("url") or entry.get("href") or entry.get("link")
            item = _social_item(platform, url, custom_label)
            if item:
                items.append(item)

    if section:
        _append_social_if_missing(items, "instagram", section.instagram_url)
        _append_social_if_missing(items, "snapchat", section.snapchat_url)
        _append_social_if_missing(items, "tiktok", section.tiktok_url)

    if site:
        for platform, url in (
            ("facebook", site.get("facebook")),
            ("instagram", site.get("instagram")),
            ("linkedin", site.get("linkedin")),
            ("snapchat", site.get("snapchat")),
            ("tiktok", site.get("tiktok")),
        ):
            _append_social_if_missing(items, platform, url)

    return _dedupe_social_by_platform(items)


def _dedupe_social_by_platform(items):
    """Keep one icon per platform (JSON / footer / site settings)."""
    by_platform = {}
    order = []
    for item in items:
        platform = item.get("platform")
        if not platform:
            continue
        if platform not in by_platform:
            order.append(platform)
        by_platform[platform] = item
    return [by_platform[platform] for platform in order]


def _split_phone_values(raw):
    if not raw:
        return []
    normalized = raw.replace("|", "/").replace("،", "/").replace(",", "/")
    return [p.strip() for p in normalized.split("/") if p.strip()]


def _parse_footer_phones(section):
    landline = (section.phone_landline or "").strip()
    mobile = (section.phone_mobile or "").strip()

    if landline and not mobile:
        extra = _split_phone_values(landline)
        if len(extra) >= 2:
            landline, mobile = extra[0], extra[1]

    if not landline and not mobile and section.phone:
        parts = _split_phone_values(section.phone)
        if len(parts) >= 2:
            landline, mobile = parts[0], parts[1]
        elif len(parts) == 1:
            landline = parts[0]
    elif landline and not mobile and section.phone:
        parts = _split_phone_values(section.phone)
        if parts:
            mobile = parts[0]
    elif mobile and not landline and section.phone:
        parts = _split_phone_values(section.phone)
        if parts:
            landline = parts[0]

    return landline, mobile


def _resolve_footer_url(url_value):
    if not url_value:
        return "#"
    url_value = str(url_value).strip()
    if url_value.startswith(("http://", "https://", "mailto:", "tel:")):
        return url_value
    if url_value.startswith("#"):
        try:
            return reverse("home") + url_value
        except NoReverseMatch:
            return url_value
    if url_value.startswith("/"):
        return url_value

    try:
        return reverse(url_value)
    except NoReverseMatch:
        pass

    # slug قسم في الصفحة الرئيسية: about → /#about
    anchor = anchor_for_slug(url_value)
    try:
        return reverse("home") + "#" + anchor
    except NoReverseMatch:
        return "#" + anchor


def _default_quick_links():
    home = reverse("home")
    return [
        {"label": _("About us"), "href": f"{home}#about"},
        {"label": _("Our services"), "href": f"{home}#services"},
        {"label": _("Our work"), "href": f"{home}#our-work"},
        {"label": _("Contact"), "href": f"{home}#simply-contact"},
        {"label": _("Home"), "href": home},
    ]


def _parse_quick_links(section):
    raw = section.quick_links if section else None
    links = []

    if isinstance(raw, list):
        for item in raw:
            if not isinstance(item, dict):
                continue
            label = (item.get("label") or item.get("title") or "").strip()
            if not label:
                continue
            href = _resolve_footer_url(item.get("url") or item.get("href") or "#")
            links.append({"label": label, "href": href})

    if not links:
        links = _default_quick_links()

    mid = (len(links) + 1) // 2
    return links[:mid], links[mid:]


def build_footer_data(section, site=None):
    site = site or {}
    if not section:
        quick_col1, quick_col2 = _parse_quick_links(None)
        return {
            "logo_url": "",
            "site_name": "",
            "description": "",
            "address": "",
            "email": "",
            "website": "",
            "map_url": "",
            "instagram_url": "",
            "phone_landline": "",
            "phone_mobile": "",
            "phone_tel_primary": "",
            "copyright_text": "",
            "quick_links_col1": quick_col1,
            "quick_links_col2": quick_col2,
            "social_links": _parse_social_links(None, site),
        }

    landline, mobile = _parse_footer_phones(section)
    tel_primary = landline or mobile
    quick_col1, quick_col2 = _parse_quick_links(section)

    return {
        "logo_url": section.logo.url if section.logo else "",
        "site_name": section.site_name or "",
        "description": section.description or "",
        "address": section.address or "",
        "email": section.email or "",
        "website": section.website or "",
        "map_url": section.map_url or "",
        "instagram_url": section.instagram_url or "",
        "phone_landline": landline,
        "phone_mobile": mobile,
        "phone_tel_primary": tel_primary.replace(" ", "") if tel_primary else "",
        "copyright_text": section.copyright_text or "",
        "quick_links_col1": quick_col1,
        "quick_links_col2": quick_col2,
        "social_links": _parse_social_links(section, site),
    }
