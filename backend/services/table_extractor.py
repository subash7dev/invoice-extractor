import re
from typing import List, Dict


class TableExtractor:
    """
    Production-grade invoice table extractor.

    Supports:
    - Digital PDFs
    - OCR text
    - Generic invoice layouts
    """

    @staticmethod
    def extract(text: str) -> List[Dict]:

        if not text:
            return []

        items = []

        lines = [

            line.strip()

            for line in text.splitlines()

            if line.strip()

        ]

        i = 0

        while i < len(lines):

            line = lines[i]

            item = TableExtractor.parse_single_line(line)

            if item:

                items.append(item)

                i += 1

                continue

            item = TableExtractor.parse_multi_line(lines, i)

            if item:

                items.append(item)

                i += item["lines_used"]

                item.pop("lines_used", None)

                continue

            i += 1

        return items

    @staticmethod
    def parse_single_line(line):

        pattern = re.compile(

            r"^(.*?)\s+(\d+(?:\.\d+)?)\s+([\d,.]+)\s+([\d,.]+)$"

        )

        match = pattern.match(line)

        if not match:

            return None

        description, qty, unit_price, amount = match.groups()

        return {

            "description": description.strip(),

            "quantity": float(qty),

            "unit_price": TableExtractor.money(unit_price),

            "amount": TableExtractor.money(amount)

        }

    @staticmethod
    def parse_multi_line(lines, index):

        if index + 3 >= len(lines):

            return None

        description = lines[index]

        qty = lines[index + 1]

        unit_price = lines[index + 2]

        amount = lines[index + 3]

        if not re.fullmatch(r"\d+(\.\d+)?", qty):

            return None

        if not TableExtractor.is_money(unit_price):

            return None

        if not TableExtractor.is_money(amount):

            return None

        return {

            "description": description,

            "quantity": float(qty),

            "unit_price": TableExtractor.money(unit_price),

            "amount": TableExtractor.money(amount),

            "lines_used": 4

        }

    @staticmethod
    def money(value):

        value = value.replace(",", "")

        value = value.replace("USD", "")

        value = value.replace("INR", "")

        value = value.replace("$", "")

        value = value.strip()

        try:

            return float(value)

        except Exception:

            return None

    @staticmethod
    def is_money(value):

        value = value.replace(",", "")

        value = value.replace("USD", "")

        value = value.replace("INR", "")

        value = value.replace("$", "")

        value = value.strip()

        return bool(

            re.fullmatch(

                r"\d+(\.\d+)?",

                value

            )

        )