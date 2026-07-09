from typing import List

import cv2
import numpy as np
from paddleocr import PaddleOCR


class OCRService:
    """
    PaddleOCR v2.8.x Service
    """

    _ocr = None

    @classmethod
    def get_engine(cls):

        if cls._ocr is None:

            cls._ocr = PaddleOCR(

                use_angle_cls=True,

                lang="en",

                show_log=False

            )

        return cls._ocr

    @classmethod
    def extract_text(cls, image):

        ocr = cls.get_engine()

        if isinstance(image, str):

            image = cv2.imread(image)

        if image is None:

            return ""

        result = ocr.ocr(

            image,

            cls=True

        )

        return cls.parse_result(result)

    @classmethod
    def extract_multiple(cls, images: List):

        texts = []

        for image in images:

            text = cls.extract_text(image)

            if text.strip():

                texts.append(text)

        return "\n\n".join(texts)

    @staticmethod
    def parse_result(result):

        if not result:

            return ""

        lines = []

        for page in result:

            if page is None:

                continue

            for item in page:

                if item is None:

                    continue

                try:

                    text = item[1][0]

                    score = item[1][1]

                    if score >= 0.50:

                        lines.append(text.strip())

                except Exception:

                    continue

        return "\n".join(lines)

    @classmethod
    def extract_with_confidence(cls, image):

        ocr = cls.get_engine()

        if isinstance(image, str):

            image = cv2.imread(image)

        if image is None:

            return []

        result = ocr.ocr(

            image,

            cls=True

        )

        words = []

        for page in result:

            if page is None:

                continue

            for item in page:

                if item is None:

                    continue

                try:

                    words.append(

                        {

                            "text": item[1][0],

                            "confidence": round(

                                float(item[1][1]),

                                3

                            )

                        }

                    )

                except Exception:

                    pass

        return words