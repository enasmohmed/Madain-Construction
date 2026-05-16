from modeltranslation.translator import translator, TranslationOptions
from .models import (
    HeroSlide,
    HomeOfferStrip,
    HomeServicesSection,
    HomeServiceCard,
    MVVPartnerLogo,
    MVVTabPanel,
    MVVTabBullet,
    FinalWordSection,
    FinalWordColumnLine,
)


class HeroSlideTranslationOptions(TranslationOptions):
    fields = ('tagline', 'heading', 'lead', 'button_text')


class HomeOfferStripTranslationOptions(TranslationOptions):
    fields = (
        "column_1_title",
        "column_1_text",
        "column_2_title",
        "column_2_text",
        "column_3_title",
        "column_3_text",
    )


class HomeServicesSectionTranslationOptions(TranslationOptions):
    fields = ("title", "subtitle", "footer_note")


class HomeServiceCardTranslationOptions(TranslationOptions):
    fields = ("title", "intro", "points")


class MVVPartnerLogoTranslationOptions(TranslationOptions):
    fields = ("alt_text",)


class MVVTabPanelTranslationOptions(TranslationOptions):
    fields = ("title", "body")


class MVVTabBulletTranslationOptions(TranslationOptions):
    fields = ("text",)


class FinalWordColumnLineTranslationOptions(TranslationOptions):
    fields = ("text",)


class FinalWordSectionTranslationOptions(TranslationOptions):
    fields = ("title", "body")


translator.register(HeroSlide, HeroSlideTranslationOptions)
translator.register(HomeOfferStrip, HomeOfferStripTranslationOptions)
translator.register(HomeServicesSection, HomeServicesSectionTranslationOptions)
translator.register(HomeServiceCard, HomeServiceCardTranslationOptions)
translator.register(MVVPartnerLogo, MVVPartnerLogoTranslationOptions)
translator.register(MVVTabPanel, MVVTabPanelTranslationOptions)
translator.register(MVVTabBullet, MVVTabBulletTranslationOptions)
translator.register(FinalWordColumnLine, FinalWordColumnLineTranslationOptions)
translator.register(FinalWordSection, FinalWordSectionTranslationOptions)
