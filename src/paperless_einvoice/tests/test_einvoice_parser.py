from pathlib import Path

import pytest
from pytest_django.fixtures import SettingsWrapper
from pytest_httpx import HTTPXMock

from paperless_einvoice.parsers import EInvoiceDocumentParser


@pytest.mark.django_db()
class TestEInvoiceParser:
    def test_parse(
        self,
        httpx_mock: HTTPXMock,
        settings: SettingsWrapper,
        einvoice_parser: EInvoiceDocumentParser,
        sample_xml_file: Path,
    ):
        return None
