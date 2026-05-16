from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'

    def ready(self):
        # modeltranslation must register before migrations / ORM use the translated fields
        import pages.translation  # noqa: F401
