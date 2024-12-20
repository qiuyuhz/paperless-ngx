from django.apps import AppConfig
from django.conf import settings

from paperless_einvoice.signals import einvoice_consumer_declaration


class PaperlessEInvoiceConfig(AppConfig):
    name = "paperless_einvoice"

    def ready(self):
        from documents.signals import document_consumer_declaration

        if settings.TIKA_ENABLED and settings.EINVOICE_PARSER_ENABLED:
            document_consumer_declaration.connect(einvoice_consumer_declaration)
        AppConfig.ready(self)
