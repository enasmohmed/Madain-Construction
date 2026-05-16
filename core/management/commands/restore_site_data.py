"""
Restore site content from fixtures/site_admin_backup.json.

Use after deploy when the live database is empty but media/ files exist on disk.
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import FooterSection, Sections, SiteSettings
from pages.models import (
    FinalWordColumnLine,
    FinalWordSection,
    HeroBannerSettings,
    HeroOverlayImage,
    HeroSlide,
    HeroSlideBackgroundImage,
    HomeOfferStrip,
    HomeServiceCard,
    HomeServicesSection,
    MissionVisionValuesBlock,
    MVVPartnerLogo,
    MVVTabBullet,
    MVVTabPanel,
    OurWorkImage,
)


class Command(BaseCommand):
    help = "Restore admin-managed home page data from fixtures/site_admin_backup.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-input",
            action="store_true",
            help="Skip confirmation prompt.",
        )

    def handle(self, *args, **options):
        if not options["no_input"]:
            confirm = input(
                "This replaces Site settings, footer, hero, services, MVV, "
                "our work, and final word records. Continue? [y/N] "
            )
            if confirm.strip().lower() not in ("y", "yes"):
                self.stdout.write(self.style.WARNING("Cancelled."))
                return

        with transaction.atomic():
            self._clear_site_content()
            call_command("loaddata", "site_admin_backup", verbosity=1)

        self.stdout.write(
            self.style.SUCCESS(
                "Site data restored. Ensure media/ files are on the server "
                "(paths in the database point under media/)."
            )
        )

    def _clear_site_content(self):
        # Children first (FK order).
        HeroSlideBackgroundImage.objects.all().delete()
        HeroOverlayImage.objects.all().delete()
        HeroSlide.objects.all().delete()
        HeroBannerSettings.objects.all().delete()
        HomeServiceCard.objects.all().delete()
        HomeServicesSection.objects.all().delete()
        HomeOfferStrip.objects.all().delete()
        MVVTabBullet.objects.all().delete()
        MVVPartnerLogo.objects.all().delete()
        MVVTabPanel.objects.all().delete()
        MissionVisionValuesBlock.objects.all().delete()
        FinalWordColumnLine.objects.all().delete()
        FinalWordSection.objects.all().delete()
        OurWorkImage.objects.all().delete()
        FooterSection.objects.all().delete()
        Sections.objects.all().delete()
        SiteSettings.objects.all().delete()
