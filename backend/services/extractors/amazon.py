from services.extractors.base import BaseExtractor
from services.amazon_parser import AmazonParser
from services.llm import LLMService


class AmazonExtractor(BaseExtractor):
    """
    Amazon Invoice Extractor

    Strategy:
    1. Amazon rule-based parser
    2. Generic parser merge
    3. LLM fills missing values
    4. Normalize output
    """

    def extract(
        self,
        text: str,
        vendor: str,
        parsed: dict,
        items: list
    ) -> dict:

        amazon_data = AmazonParser.extract(text)

        parser_data = {}

        parser_data.update(parsed)

        parser_data.update(

            {

                key: value

                for key, value in amazon_data.items()

                if value not in (None, "", [])

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