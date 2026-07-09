from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """
    Base class for all vendor extractors.

    Each extractor receives:
        - OCR text
        - Vendor name
        - Rule parser output
        - Table items

    Returns:
        Dictionary representing the invoice.
    """

    @abstractmethod
    def extract(
        self,
        text: str,
        vendor: str,
        parsed: dict,
        items: list
    ) -> dict:
        """
        Extract structured invoice data.

        Must be implemented by subclasses.
        """
        raise NotImplementedError

    @staticmethod
    def merge(
        llm_result: dict,
        parser_result: dict,
        items: list
    ) -> dict:
        """
        Merge parser values into LLM output.
        """

        result = llm_result.copy()

        for key, value in parser_result.items():

            if value in (None, "", []):
                continue

            if result.get(key) in (None, "", []):

                result[key] = value

        if items:

            if not result.get("items"):

                result["items"] = items

        return result

    @staticmethod
    def clean(invoice: dict) -> dict:
        """
        Remove empty strings and normalize values.
        """

        cleaned = {}

        for key, value in invoice.items():

            if isinstance(value, str):

                value = value.strip()

                if value == "":
                    value = None

            cleaned[key] = value

        return cleaned

    @staticmethod
    def normalize_currency(invoice: dict):

        currency = invoice.get("currency")

        if currency:

            invoice["currency"] = currency.upper()

        return invoice