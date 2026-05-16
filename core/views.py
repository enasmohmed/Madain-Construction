from django.contrib import messages
from django.db.models import Prefetch
from django.utils.translation import gettext as _
from django.views.generic import FormView
from contact.forms import HomeContactForm
from contact.services import submit_contact_message
from pages.models import (
    HeroBannerSettings,
    HeroSlide,
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


class HomeView(FormView):
    template_name = 'pages/index.html'
    form_class = HomeContactForm

    def _offer_strip_for_request(self):
        lang = getattr(self.request, "LANGUAGE_CODE", None) or "ar"
        qs = HomeOfferStrip.objects.filter(is_active=True)
        return qs.filter(language=lang).first() or qs.first()

    def _services_section_for_request(self):
        lang = getattr(self.request, "LANGUAGE_CODE", None) or "ar"
        card_qs = HomeServiceCard.objects.filter(is_active=True).order_by("order", "id")
        base_qs = HomeServicesSection.objects.filter(is_active=True).prefetch_related(
            Prefetch("cards", queryset=card_qs),
        )
        section = base_qs.filter(language=lang).first()
        if section and section.cards.all():
            return section
        for candidate in base_qs.order_by("-language", "id"):
            if candidate.cards.all():
                return candidate
        return section or base_qs.first()

    def _mvv_block_for_request(self):
        lang = getattr(self.request, "LANGUAGE_CODE", None) or "ar"
        qs = MissionVisionValuesBlock.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                "partner_logos",
                queryset=MVVPartnerLogo.objects.order_by("order", "id"),
            ),
            Prefetch(
                "tab_panels",
                queryset=MVVTabPanel.objects.order_by("order", "id").prefetch_related(
                    Prefetch(
                        "bullets",
                        queryset=MVVTabBullet.objects.order_by("order", "id"),
                    )
                ),
            ),
        )
        return qs.filter(language=lang).first() or qs.first()

    def _final_word_for_request(self):
        lang = getattr(self.request, "LANGUAGE_CODE", None) or "ar"
        qs = FinalWordSection.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                "column_lines",
                queryset=FinalWordColumnLine.objects.order_by("order", "id"),
            )
        )
        return qs.filter(language=lang).first() or qs.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['hero_slides'] = HeroSlide.objects.filter(is_active=True).order_by('order', 'id').prefetch_related(
            'extra_backgrounds',
        )
        hero_banner = HeroBannerSettings.objects.prefetch_related(
            "overlay_images",
        ).first()
        context['hero_banner'] = hero_banner
        context['offer_strip'] = self._offer_strip_for_request()
        context['use_hero_video'] = bool(
            hero_banner
            and hero_banner.prefer_video
            and (hero_banner.external_video_url or hero_banner.background_video)
        )
        work_items = [
            o
            for o in OurWorkImage.objects.filter(is_active=True).order_by("order", "id")
            if o.image or o.video
        ]
        context["our_work_images"] = work_items
        columns = [[] for _ in range(4)]
        for i, o in enumerate(work_items):
            columns[i % 4].append(o)
        context["our_work_columns"] = [c for c in columns if c]
        services_section = self._services_section_for_request()
        context["services_section"] = services_section
        context["services_cards"] = (
            list(services_section.cards.all()) if services_section else []
        )
        context["mvv_block"] = self._mvv_block_for_request()
        context["final_word_section"] = self._final_word_for_request()
        return context

    def get_success_url(self):
        return f"{self.request.path}#simply-contact"

    def form_valid(self, form):
        data = form.cleaned_data
        try:
            submit_contact_message(
                name=data["name"],
                email=data["email"],
                message=data["message"],
            )
        except Exception:
            messages.error(
                self.request,
                _("We could not send your message. Please try again later."),
                extra_tags="contact",
            )
            return self.form_invalid(form)

        messages.success(
            self.request,
            _("Your message was sent successfully. We will get back to you soon."),
            extra_tags="contact",
        )
        return super().form_valid(form)
