from services.extractors.base import BaseExtractor
from services.bmi_parser import BMIParser
from services.llm import LLMService


class BMIExtractor(BaseExtractor):
    """
    BMI Vendor Extractor

    Strategy:
    1. Rule-based parser extracts deterministic fields.
    2. LLM extracts missing fields.
    3. Merge parser + LLM.
    4. Normalize output.
    """

    def extract(
        self,
        text: str,
        vendor: str,
        parsed: dict,
        items: list
    ) -> dict:

        bmi_data = BMIParser.extract(text)

        parser_data = {}

        parser_data.update(parsed)

        parser_data.update(

            {

                k: v

                for k, v in bmi_data.items()

                if v not in (None, "", [])

            }

        )

        llm_result = LLMService.extract(

            text=text,

            vendor=vendor,

            detected_items=items,

            parsed_fields=parser_data

        )

        invoice = self.merge(

            llm_result,

            parser_data,

            items

        )

        invoice = self.normalize_currency(invoice)

        invoice = self.clean(invoice)

        return invoice