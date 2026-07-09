import json
import re
from pathlib import Path


class VendorDetector:
    """
    Detect invoice vendor using keyword scoring.
    """

    CONFIG_PATH = Path("config/vendors.json")

    _vendors = None

    @classmethod
    def load_config(cls):

        if cls._vendors is not None:
            return cls._vendors

        if cls.CONFIG_PATH.exists():

            with open(
                cls.CONFIG_PATH,
                "r",
                encoding="utf-8"
            ) as f:

                cls._vendors = json.load(f)

        else:

            cls._vendors = {}

        return cls._vendors

    @staticmethod
    def normalize(text: str) -> str:

        text = text.lower()

        text = re.sub(r"\s+", " ", text)

        return text

    @classmethod
    def detect(cls, text: str) -> str:

        text = cls.normalize(text)

        vendors = cls.load_config()

        best_vendor = "Generic"

        best_score = 0

        for vendor, keywords in vendors.items():

            score = 0

            for keyword in keywords:

                keyword = keyword.lower()

                if keyword in text:

                    score += 1

            if score > best_score:

                best_score = score

                best_vendor = vendor

        return best_vendor

    @classmethod
    def score(cls, text: str):

        text = cls.normalize(text)

        vendors = cls.load_config()

        scores = {}

        for vendor, keywords in vendors.items():

            score = 0

            for keyword in keywords:

                if keyword.lower() in text:

                    score += 1

            scores[vendor] = score

        return dict(

            sorted(

                scores.items(),

                key=lambda x: x[1],

                reverse=True

            )

        )

    @classmethod
    def available_vendors(cls):

        return list(

            cls.load_config().keys()

        )

    @classmethod
    def is_supported(cls, vendor: str):

        return vendor in cls.load_config()