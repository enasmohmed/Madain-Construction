"""Landing-page section slugs → HTML anchor ids (shared by navbar & footer links)."""

HOME_ANCHOR_ALIASES = {
    "home": "hero",
    "about": "about",
    "من-نحن": "about",
    "services": "services",
    "خدماتنا": "services",
    "our-services": "services",
    "portfolio": "our-work",
    "معرض-الاعمال": "our-work",
    "معرض-الأعمال": "our-work",
    "our-work": "our-work",
    "projects": "our-work",
    "company-vision": "vision",
    "vision": "vision",
    "رؤية-الشركة": "vision",
    "company-mission": "mission",
    "mission": "mission",
    "رسالة-الشركة": "mission",
    "values": "values",
    "contact": "simply-contact",
    "simply-contact": "simply-contact",
    "final-word": "final-word",
    "blog": "final-word",
}


def anchor_for_slug(slug):
    if not slug:
        return "hero"
    normalized = str(slug).strip().lower().lstrip("/").lstrip("#")
    return HOME_ANCHOR_ALIASES.get(normalized, normalized)
