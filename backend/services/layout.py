from paddleocr import PPStructure

class LayoutAnalyzer:

    def __init__(self):

        self.engine = PPStructure(
            show_log=False,
            layout=True,
            table=True,
            ocr=True
        )

    def analyze(self, image):

        return self.engine(image)