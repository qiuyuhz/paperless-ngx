def get_parser(*args, **kwargs):
    from paperless_einvoice.parsers import EInvoiceDocumentParser

    return EInvoiceDocumentParser(*args, **kwargs)


def einvoice_consumer_declaration(sender, **kwargs):
    return {
        "parser": get_parser,
        "weight": 10,
        "mime_types": {
            "text/xml": ".xml",
            "application/xml": ".xml",
        },
    }
