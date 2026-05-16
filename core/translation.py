from modeltranslation.translator import translator, TranslationOptions
from .models import SiteSettings, Sections


class SiteSettingsTranslationOptions(TranslationOptions):
    fields = (
        "site_name",
        "address",
        "working_hours",
        "our_work_section_title",
        "our_work_section_subtitle",
    )


class SectionsTranslationOptions(TranslationOptions):
    fields = ('title', 'slug')


translator.register(SiteSettings, SiteSettingsTranslationOptions)
translator.register(Sections, SectionsTranslationOptions)
