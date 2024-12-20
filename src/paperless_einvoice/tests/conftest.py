from collections.abc import Generator
from pathlib import Path

import pytest

from paperless_einvoice.parsers import EInvoiceDocumentParser


@pytest.fixture()
def einvoice_parser() -> Generator[EInvoiceDocumentParser, None, None]:
    try:
        parser = EInvoiceDocumentParser(logging_group=None)
        yield parser
    finally:
        parser.cleanup()


@pytest.fixture(scope="session")
def sample_dir() -> Path:
    return (Path(__file__).parent / Path("samples")).resolve()


@pytest.fixture(scope="session")
def sample_xml_file(sample_dir: Path) -> Path:
    return sample_dir / "zugferd_2p1_BASIC-WL_Einfach.xml"
