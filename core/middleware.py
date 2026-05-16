"""Force site UI language to Arabic (ignore browser Accept-Language)."""

from django.conf import settings
from django.utils import translation


class ForceArabicLanguageMiddleware:
    """
    This site is Arabic-only. LocaleMiddleware may pick English from the
    browser; run this immediately after it to keep templates, RTL, and
    modeltranslation on Arabic.
    """

    language_code = getattr(settings, "FORCE_SITE_LANGUAGE", "ar")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        translation.activate(self.language_code)
        request.LANGUAGE_CODE = self.language_code
        response = self.get_response(request)
        response.headers.setdefault("Content-Language", self.language_code)
        return response
