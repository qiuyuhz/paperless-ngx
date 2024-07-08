import json

import pytest
from django.test import override_settings
from pytest_django.fixtures import SettingsWrapper

from paperless.models import ApplicationConfiguration
from paperless.models import CleanChoices
from paperless.models import ColorConvertChoices
from paperless.models import ModeChoices
from paperless.models import OutputTypeChoices
from paperless_tesseract.parsers import RasterisedDocumentParser


@pytest.mark.django_db()
class TestParserSettingsFromDb:
    @staticmethod
    def get_params():
        """
        Helper to get just the OCRMyPDF parameters from the parser
        """
        return RasterisedDocumentParser(None).construct_ocrmypdf_parameters(
            input_file="input.pdf",
            output_file="output.pdf",
            sidecar_file="sidecar.txt",
            mime_type="application/pdf",
            safe_fallback=False,
        )

    # TODO: Make a fixture?
    @staticmethod
    def get_application_config() -> ApplicationConfiguration:
        instance = ApplicationConfiguration.objects.first()
        assert instance is not None
        return instance

    def test_db_settings_ocr_pages(self, settings: SettingsWrapper):
        """
        GIVEN:
            - Django settings defines different value for OCR_PAGES than
              configuration object
        WHEN:
            - OCR parameters are constructed
        THEN:
            - Configuration from database is utilized
        """
        settings.OCR_PAGES = 10
        instance = self.get_application_config()
        instance.pages = 5
        instance.save()

        params = self.get_params()

        assert params["pages"] == "1-5"

    def test_db_settings_ocr_language(self, settings: SettingsWrapper):
        """
        GIVEN:
            - Django settings defines different value for OCR_LANGUAGE than
              configuration object
        WHEN:
            - OCR parameters are constructed
        THEN:
            - Configuration from database is utilized
        """
        settings.OCR_LANGUAGE = "eng+deu"

        instance = self.get_application_config()
        instance.language = "fra+ita"
        instance.save()

        params = self.get_params()

        assert params["language"] == "fra+ita"

    def test_db_settings_ocr_output_type(self, settings: SettingsWrapper):
        """
        GIVEN:
            - Django settings defines different value for OCR_OUTPUT_TYPE than
              configuration object
        WHEN:
            - OCR parameters are constructed
        THEN:
            - Configuration from database is utilized
        """
        settings.OCR_OUTPUT_TYPE = "pdfa-3"
        instance = self.get_application_config()
        instance.output_type = OutputTypeChoices.PDF_A
        instance.save()

        params = self.get_params()

        assert params["output_type"] == "pdfa"

    def test_db_settings_ocr_mode(self, settings: SettingsWrapper):
        """
        GIVEN:
            - Django settings defines different value for OCR_MODE than
              configuration object
        WHEN:
            - OCR parameters are constructed
        THEN:
            - Configuration from database is utilized
        """
        settings.OCR_MODE = "redo"
        instance = self.get_application_config()
        instance.mode = ModeChoices.SKIP
        instance.save()

        params = self.get_params()

        assert params["skip_text"]
        assert "redo_ocr" not in params
        assert "force_ocr" not in params

    def test_db_settings_ocr_clean(self, settings: SettingsWrapper):
        """
        GIVEN:
            - Django settings defines different value for OCR_CLEAN than
              configuration object
        WHEN:
            - OCR parameters are constructed
        THEN:
            - Configuration from database is utilized
        """
        settings.OCR_CLEAN = CleanChoices.FINAL.value
        instance = self.get_application_config()
        instance.unpaper_clean = CleanChoices.CLEAN
        instance.save()

        params = self.get_params()

        assert params["clean"]
        assert "clean_final" not in params

        with override_settings(OCR_CLEAN="clean-final"):
            instance = self.get_application_config()
            instance.unpaper_clean = CleanChoices.FINAL
            instance.save()

            params = self.get_params()
        assert params["clean_final"]
        assert "clean" not in params

    def test_db_settings_ocr_deskew(self, settings: SettingsWrapper):
        """
        GIVEN:
            - Django settings defines different value for OCR_DESKEW than
              configuration object
        WHEN:
            - OCR parameters are constructed
        THEN:
            - Configuration from database is utilized
        """
        settings.OCR_DESKEW = False
        instance = self.get_application_config()
        instance.deskew = True
        instance.save()

        params = self.get_params()

        assert params["deskew"]

    def test_db_settings_ocr_rotate(self, settings: SettingsWrapper):
        """
        GIVEN:
            - Django settings defines different value for OCR_ROTATE_PAGES
              and OCR_ROTATE_PAGES_THRESHOLD than configuration object
        WHEN:
            - OCR parameters are constructed
        THEN:
            - Configuration from database is utilized
        """
        settings.OCR_ROTATE_PAGES = False
        settings.OCR_ROTATE_PAGES_THRESHOLD = 30.0
        instance = self.get_application_config()
        instance.rotate_pages = True
        instance.rotate_pages_threshold = 15.0
        instance.save()

        params = self.get_params()

        assert params["rotate_pages"]
        assert params["rotate_pages_threshold"] == pytest.approx(15.0)

    def test_db_settings_ocr_max_pixels(self, settings: SettingsWrapper):
        """
        GIVEN:
            - Django settings defines different value for OCR_MAX_IMAGE_PIXELS than
              configuration object
        WHEN:
            - OCR parameters are constructed
        THEN:
            - Configuration from database is utilized
        """
        settings.OCR_MAX_IMAGE_PIXELS = 2_000_000.0
        instance = self.get_application_config()
        instance.max_image_pixels = 1_000_000.0
        instance.save()

        params = self.get_params()

        assert params["max_image_mpixels"] == pytest.approx(1.0)

    def test_db_settings_ocr_color_convert(self, settings: SettingsWrapper):
        """
        GIVEN:
            - Django settings defines different value for OCR_COLOR_CONVERSION_STRATEGY than
              configuration object
        WHEN:
            - OCR parameters are constructed
        THEN:
            - Configuration from database is utilized
        """
        settings.OCR_COLOR_CONVERSION_STRATEGY = ColorConvertChoices.UNCHANGED.value
        instance = self.get_application_config()
        instance.color_conversion_strategy = ColorConvertChoices.INDEPENDENT
        instance.save()

        params = self.get_params()

        assert (
            params["color_conversion_strategy"] == ColorConvertChoices.INDEPENDENT.value
        )

    def test_ocr_user_args(self, settings: SettingsWrapper):
        """
        GIVEN:
            - Django settings defines different value for OCR_USER_ARGS than
              configuration object
        WHEN:
            - OCR parameters are constructed
        THEN:
            - Configuration from database is utilized
        """
        settings.OCR_USER_ARGS = json.dumps({"continue_on_soft_render_error": True})
        instance = self.get_application_config()
        instance.user_args = {"unpaper_args": "--pre-rotate 90"}
        instance.save()

        params = self.get_params()

        assert "unpaper_args" in params
        assert params["unpaper_args"] == "--pre-rotate 90"
