from services.extractors.base import BaseExtractor
from services.llm import LLMService


class ABCExtractor(BaseExtractor):
    """
    ABC Vendor Extractor

    Generic implementation for ABC invoices.
    Can later be extended with abc_parser.py.
    """

    def extract(
        self,
        text: str,
        vendor: str,
        parsed: dict,
        items: list
    ) -> dict:

        llm_result = LLMService.extract(

            text=text,

            vendor=vendor,

            detected_items=items,

            parsed_fields=parsed

        )

        invoice = self.merge(

            llm_result,

            parsed,

            items

        )

        invoice = self.normalize_currency(invoice)

        invoice = self.clean(invoice)

        return invoice