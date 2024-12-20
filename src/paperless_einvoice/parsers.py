from pathlib import Path

from django.conf import settings
from drafthorse.models.document import Document
from gotenberg_client import GotenbergClient
from gotenberg_client.options import MarginType
from gotenberg_client.options import MarginUnitType
from gotenberg_client.options import PageMarginsType
from gotenberg_client.options import PageSize
from gotenberg_client.options import PdfAFormat
from jinja2 import Template

from documents.parsers import ParseError
from paperless.models import OutputTypeChoices
from paperless_tika.parsers import TikaDocumentParser


class EInvoiceDocumentParser(TikaDocumentParser):
    """
    This parser parses e-invoices using Tika and Gotenberg
    """

    logging_name = "paperless.parsing.einvoice"

    def convert_to_pdf(self, document_path: Path, file_name):
        pdf_path = Path(self.tempdir) / "convert.pdf"
        self.log.info(f"Converting {document_path} to PDF as {pdf_path}")

        with document_path.open("r") as f:
            xml = f.read().encode("utf-8")
            invoice = Document.parse(xml)
            context = {
                "id": invoice.trade.agreement.seller.name,
            }
            template = Template("templates/invoice.j2.html")
            html_file = Path(self.tempdir) / "invoice_as_html.html"
            html_file.write_text(
                template.render(context),
            )

            with (
                GotenbergClient(
                    host=settings.TIKA_GOTENBERG_ENDPOINT,
                    timeout=settings.CELERY_TASK_TIME_LIMIT,
                ) as client,
                client.chromium.html_to_pdf() as route,
            ):
                # Set the output format of the resulting PDF
                if settings.OCR_OUTPUT_TYPE in {
                    OutputTypeChoices.PDF_A,
                    OutputTypeChoices.PDF_A2,
                }:
                    route.pdf_format(PdfAFormat.A2b)
                elif settings.OCR_OUTPUT_TYPE == OutputTypeChoices.PDF_A1:
                    self.log.warning(
                        "Gotenberg does not support PDF/A-1a, choosing PDF/A-2b instead",
                    )
                    route.pdf_format(PdfAFormat.A2b)
                elif settings.OCR_OUTPUT_TYPE == OutputTypeChoices.PDF_A3:
                    route.pdf_format(PdfAFormat.A3b)

                try:
                    response = (
                        route.index(html_file)
                        .resource(Path(__file__).parent / "templates" / "invoice.css")
                        .margins(
                            PageMarginsType(
                                top=MarginType(0.1, MarginUnitType.Inches),
                                bottom=MarginType(0.1, MarginUnitType.Inches),
                                left=MarginType(0.1, MarginUnitType.Inches),
                                right=MarginType(0.1, MarginUnitType.Inches),
                            ),
                        )
                        .size(PageSize(height=11.7, width=8.27))
                        .scale(1.0)
                        .run()
                    )

                    pdf_path.write_bytes(response.content)

                    return pdf_path

                except Exception as err:
                    raise ParseError(
                        f"Error while converting document to PDF: {err}",
                    ) from err
