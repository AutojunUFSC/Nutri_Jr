from django.apps import AppConfig


class FichasConfig(AppConfig):
    name = 'fichas'

    def ready(self):
        from . import signals  # noqa: F401 - registra os receivers de post_save/post_delete
