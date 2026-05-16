from django import template
from django.urls import NoReverseMatch, reverse

from core.home_anchors import anchor_for_slug

register = template.Library()


@register.simple_tag(takes_context=True)
def nav_section_url(context, section):
    """رابط مرساة لقسم في الصفحة الرئيسية (landing page)."""
    slug_raw = getattr(section, 'slug', None) or ''
    slug = slug_raw.strip().lower()
    anchor = anchor_for_slug(slug) if slug else 'hero'

    request = context.get('request')
    on_home = (
        request is not None
        and getattr(request, 'resolver_match', None) is not None
        and request.resolver_match.url_name == 'home'
    )

    if on_home:
        return '#' + anchor

    try:
        return reverse('home') + '#' + anchor
    except NoReverseMatch:
        return '#' + anchor
