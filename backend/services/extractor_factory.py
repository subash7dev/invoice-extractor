from services.extractors.base import BaseExtractor
from services.extractors.generic import GenericExtractor
from services.extractors.amazon import AmazonExtractor
from services.extractors.bmi import BMIExtractor
from services.extractors.scanapps import ScanAppsExtractor
from services.extractors.abc import ABCExtractor


class ExtractorFactory:
    """
    Factory for selecting the appropriate vendor extractor.
    """

    _extractors = {

        "amazon": AmazonExtractor,

        "bmi": BMIExtractor,

        "scanapps": ScanAppsExtractor,

        "abc": ABCExtractor,

        "generic": GenericExtractor
    }

    @classmethod
    def get(cls, vendor: str) -> BaseExtractor:

        if not vendor:

            return GenericExtractor()

        vendor = vendor.lower().strip()

        extractor = cls._extractors.get(
            vendor,
            GenericExtractor
        )

        return extractor()

    @classmethod
    def register(

        cls,

        vendor: str,

        extractor: type

    ):

        if not issubclass(extractor, BaseExtractor):

            raise TypeError(

                "Extractor must inherit BaseExtractor."

            )

        cls._extractors[

            vendor.lower().strip()

        ] = extractor

    @classmethod
    def available(cls):

        return sorted(

            cls._extractors.keys()

        )