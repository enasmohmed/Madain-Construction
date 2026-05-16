from django.apps import AppConfig


def _sqlite_pragmas(sender, connection, **kwargs):
    """WAL + synchronous=NORMAL يُحسّن القراءة/الكتابة مع SQLite خصوصًا على أقراص بطيئة أو خارجية."""
    if connection.vendor != "sqlite":
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
    except Exception:
        pass


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        import core.translation  # noqa: F401

        from django.db.backends.signals import connection_created

        connection_created.connect(_sqlite_pragmas, dispatch_uid="core_sqlite_pragmas")

        # إبطال كاش رأس/تذييل عند تغيير البيانات من الأدمن
        from django.core.cache import cache
        from django.db.models.signals import post_delete, post_save

        from core import context_processors as site_ctx
        from core.models import FooterSection, Sections, SiteSettings

        def bust_site_layout_cache(**kwargs):
            cache.delete(site_ctx._SITE_CONTEXT_CACHE_KEY)

        for model in (SiteSettings, Sections, FooterSection):
            uid = f"core_bust_layout_{model._meta.label}"
            post_save.connect(bust_site_layout_cache, sender=model, dispatch_uid=uid)
            post_delete.connect(bust_site_layout_cache, sender=model, dispatch_uid=f"{uid}_del")
