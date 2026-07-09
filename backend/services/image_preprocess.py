from pathlib import Path

import cv2
import numpy as np


class ImagePreprocessor:
    """
    Production-grade image preprocessing for OCR.
    """

    @classmethod
    def preprocess(cls, image_path: str):

        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(f"Unable to read image: {image_path}")

        image = cls.resize(image)

        gray = cls.to_gray(image)

        gray = cls.remove_noise(gray)

        gray = cls.enhance_contrast(gray)

        gray = cls.threshold(gray)

        gray = cls.deskew(gray)

        return gray

    @staticmethod
    def resize(image, max_width=1800):

        h, w = image.shape[:2]

        if w <= max_width:
            return image

        ratio = max_width / w

        return cv2.resize(
            image,
            (
                int(w * ratio),
                int(h * ratio)
            ),
            interpolation=cv2.INTER_CUBIC
        )

    @staticmethod
    def to_gray(image):

        if len(image.shape) == 2:
            return image

        return cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

    @staticmethod
    def remove_noise(gray):

        return cv2.fastNlMeansDenoising(
            gray,
            None,
            15,
            7,
            21
        )

    @staticmethod
    def enhance_contrast(gray):

        clahe = cv2.createCLAHE(
            clipLimit=2.5,
            tileGridSize=(8, 8)
        )

        return clahe.apply(gray)

    @staticmethod
    def threshold(gray):

        return cv2.adaptiveThreshold(

            gray,

            255,

            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

            cv2.THRESH_BINARY,

            31,

            15
        )

    @staticmethod
    def deskew(image):

        coords = np.column_stack(np.where(image < 255))

        if len(coords) == 0:
            return image

        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = 90 + angle

        elif angle > 45:
            angle = angle - 90

        else:
            angle = angle

        (h, w) = image.shape[:2]

        center = (w // 2, h // 2)

        matrix = cv2.getRotationMatrix2D(
            center,
            angle,
            1.0
        )

        return cv2.warpAffine(

            image,

            matrix,

            (w, h),

            flags=cv2.INTER_CUBIC,

            borderMode=cv2.BORDER_REPLICATE
        )

    @staticmethod
    def save(image, output_path):

        output = Path(output_path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        cv2.imwrite(str(output), image)

        return str(output)