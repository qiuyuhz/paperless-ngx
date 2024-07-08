from collections.abc import Generator
from pathlib import Path

import pytest
from pytest_django.fixtures import SettingsWrapper
from pytest_mock import MockerFixture

from paperless.config import OcrConfig
from paperless_tesseract.parsers import RasterisedDocumentParser


@pytest.fixture()
def tesseract_parser() -> Generator[RasterisedDocumentParser, None, None]:
    try:
        parser = RasterisedDocumentParser(logging_group=None)
        yield parser
    finally:
        if "parser" in locals():
            parser.cleanup()


@pytest.fixture()
def dummy_ocr_settings(mocker: MockerFixture, settings: SettingsWrapper) -> OcrConfig:
    """
    Prevents access to the database, preferring the settings values instead
    """

    def inner():
        mocker.patch("paperless.config.OcrConfig.__post_init__")
        obj = OcrConfig()
        obj.output_type = settings.OCR_OUTPUT_TYPE
        obj.pages = settings.OCR_PAGES
        obj.language = settings.OCR_LANGUAGE
        obj.mode = settings.OCR_MODE
        obj.skip_archive_file = settings.OCR_SKIP_ARCHIVE_FILE
        obj.image_dpi = settings.OCR_IMAGE_DPI
        obj.clean = settings.OCR_CLEAN
        obj.deskew = settings.OCR_DESKEW
        obj.rotate = settings.OCR_ROTATE_PAGES
        obj.rotate_threshold = settings.OCR_ROTATE_PAGES_THRESHOLD
        obj.max_image_pixel = settings.OCR_MAX_IMAGE_PIXELS
        obj.color_conversion_strategy = settings.OCR_COLOR_CONVERSION_STRATEGY
        obj.user_args = None
        return obj

    return inner


@pytest.fixture()
def tesseract_parser_no_db_factory(
    mocker: MockerFixture,
    dummy_ocr_settings: OcrConfig,
) -> type[RasterisedDocumentParser]:
    """
    A Tesseract based parser, except it does not require the database.  It is patched to
    always use settings.
    """
    mocker.patch(
        "paperless_tesseract.parsers.RasterisedDocumentParser.get_settings",
    ).side_effect = dummy_ocr_settings
    return RasterisedDocumentParser


@pytest.fixture(scope="session")
def sample_dir() -> Path:
    return (Path(__file__).parent / Path("samples")).resolve()


@pytest.fixture(scope="session")
def simple_digital_pdf(sample_dir: Path) -> Path:
    return sample_dir / "simple-digital.pdf"


@pytest.fixture(scope="session")
def encrypted_digital_pdf(sample_dir: Path) -> Path:
    return sample_dir / "encrypted.pdf"


@pytest.fixture(scope="session")
def multi_page_digital_pdf(sample_dir: Path) -> Path:
    return sample_dir / "multi-page-digital.pdf"


@pytest.fixture(scope="session")
def multi_page_images_pdf(sample_dir: Path) -> Path:
    return sample_dir / "multi-page-images.pdf"


@pytest.fixture(scope="session")
def multi_page_mixed_pdf(sample_dir: Path) -> Path:
    return sample_dir / "multi-page-mixed.pdf"


@pytest.fixture(scope="session")
def single_page_mixed_pdf(sample_dir: Path) -> Path:
    return sample_dir / "single-page-mixed.pdf"


@pytest.fixture(scope="session")
def rotated_pdf(sample_dir: Path) -> Path:
    return sample_dir / "rotated.pdf"


@pytest.fixture(scope="session")
def rtl_pdf(sample_dir: Path) -> Path:
    return sample_dir / "rtl-test.pdf"


@pytest.fixture(scope="session")
def multi_page_tiff(sample_dir: Path) -> Path:
    return sample_dir / "multi-page-images.tiff"


@pytest.fixture(scope="session")
def multi_page_alpha_tiff(sample_dir: Path) -> Path:
    return sample_dir / "multi-page-images-alpha.tiff"


@pytest.fixture(scope="session")
def multi_page_rgb_tiff(sample_dir: Path) -> Path:
    return sample_dir / "multi-page-images-alpha-rgb.tiff"


@pytest.fixture(scope="session")
def pdf_with_form(sample_dir: Path) -> Path:
    return sample_dir / "with-form.pdf"


@pytest.fixture(scope="session")
def signed_pdf(sample_dir: Path) -> Path:
    return sample_dir / "signed.pdf"


@pytest.fixture(scope="session")
def simple_no_dpi_png(sample_dir: Path) -> Path:
    return sample_dir / "simple-no-dpi.png"


@pytest.fixture(scope="session")
def simple_png(sample_dir: Path) -> Path:
    return sample_dir / "simple.png"


@pytest.fixture(scope="session")
def simple_bmp(sample_dir: Path) -> Path:
    return sample_dir / "simple.bmp"


@pytest.fixture(scope="session")
def simple_jpeg(sample_dir: Path) -> Path:
    return sample_dir / "simple.jpg"


@pytest.fixture(scope="session")
def simple_gif(sample_dir: Path) -> Path:
    return sample_dir / "simple.gif"


@pytest.fixture(scope="session")
def simple_tiff(sample_dir: Path) -> Path:
    return sample_dir / "simple.tif"


@pytest.fixture(scope="session")
def simple_webp(sample_dir: Path) -> Path:
    return sample_dir / "simple.webp"


@pytest.fixture(scope="session")
def png_with_alpha(sample_dir: Path) -> Path:
    return sample_dir / "simple-alpha.png"
