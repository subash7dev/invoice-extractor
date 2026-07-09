from pathlib import Path
import time
import traceback

from services.file_handler import FileHandler
from services.pdf_detector import PDFDetector
from services.pdf_text import PDFTextExtractor
from services.pdf_to_image import PDFToImage
from services.image_preprocess import ImagePreprocessor
from services.ocr import OCRService
from services.cleanup import TextCleaner
from services.parser import InvoiceParser
from services.table_extractor import TableExtractor
from services.vendor_detector import VendorDetector
from services.extractor_factory import ExtractorFactory
from services.validator import InvoiceValidator
from services.confidence import ConfidenceScorer
from services.exporter import Exporter


class InvoicePipeline:
    """
    Production-grade invoice extraction pipeline.
    """

    def __init__(self):

        self.upload_dir = Path("uploads")

        self.output_dir = Path("outputs")

        self.upload_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def process(self, file_path: str):

        start = time.perf_counter()

        try:

            # =====================================================
            # FILE TYPE
            # =====================================================

            file_type = FileHandler.get_file_type(file_path)

            text = ""

            # =====================================================
            # IMAGE
            # =====================================================

            if file_type == "image":

                print("\n📷 Processing Image...\n")

                t = time.perf_counter()
                processed_image = ImagePreprocessor.preprocess(
                    file_path
                )

                text = OCRService.extract_text(
                    processed_image
                )
                print(f"OCR               : {time.perf_counter()-t:.2f}s")

            # =====================================================
            # PDF
            # =====================================================

            elif file_type == "pdf":

                pdf_info = PDFDetector.analyze(file_path)

                print("\n======================================")

                print(" PDF ANALYSIS")

                print("======================================")

                print(
                    f"Type           : {pdf_info['pdf_type']}"
                )

                print(
                    f"Pages          : {pdf_info['total_pages']}"
                )

                print(
                    f"Digital Pages  : {pdf_info['digital_pages']}"
                )

                print(
                    f"Scanned Pages  : {pdf_info['scanned_pages']}"
                )

                print("======================================\n")

                # ---------------------------------------------
                if pdf_info["pdf_type"] == "digital":

                    t = time.perf_counter()
                    text = PDFTextExtractor.extract(
                        file_path
                    )
                    print(f"PDF Text          : {time.perf_counter()-t:.2f}s")

                # ---------------------------------------------
                elif pdf_info["pdf_type"] == "scanned":

                    t = time.perf_counter()
                    images = PDFToImage.convert(
                        file_path,
                        str(self.upload_dir)
                    )

                    processed_pages = []

                    for image in images:

                        processed = ImagePreprocessor.preprocess(
                            image
                        )

                        processed_pages.append(processed)

                    text = OCRService.extract_multiple(
                        processed_pages
                    )
                    print(f"OCR               : {time.perf_counter()-t:.2f}s")

                # ---------------------------------------------
                else:

                    t = time.perf_counter()
                    # Extract digital text from digital pages only
                    digital_text = PDFTextExtractor.extract_by_page_types(
                        file_path,
                        pdf_info["pages"]
                    )

                    # OCR only scanned pages
                    scanned_pages = [
                        p for p in pdf_info["pages"]
                        if p["type"] == "scanned"
                    ]

                    ocr_texts = []
                    for page_info in scanned_pages:
                        page_num = page_info["page"]
                        image = PDFToImage.convert_page(
                            file_path,
                            page_num,
                            str(self.upload_dir)
                        )
                        processed = ImagePreprocessor.preprocess(image)
                        ocr_text = OCRService.extract_text(processed)
                        if ocr_text.strip():
                            ocr_texts.append(ocr_text)

                    ocr_text = "\n\n".join(ocr_texts)
                    print(f"OCR (scanned)     : {time.perf_counter()-t:.2f}s")

                    # Merge both texts
                    text = digital_text
                    if ocr_text:
                        text = f"{digital_text}\n\n{ocr_text}" if digital_text else ocr_text

            # =====================================================
            else:

                raise ValueError(
                    f"Unsupported file type: {file_type}"
                )

            # =====================================================
            # CLEAN TEXT
            # =====================================================

            t = time.perf_counter()
            text = TextCleaner.clean(text)
            print(f"Text Cleanup      : {time.perf_counter()-t:.2f}s")

            if not text.strip():

                raise Exception(
                    "No text extracted from document."
                )

            # =====================================================
            # RULE PARSER
            # =====================================================

            t = time.perf_counter()
            parsed_fields = InvoiceParser.extract(
                text
            )
            print(f"Parser            : {time.perf_counter()-t:.2f}s")

            # =====================================================
            # TABLE EXTRACTION
            # =====================================================

            t = time.perf_counter()
            items = TableExtractor.extract(
                text
            )
            print(f"Table Extraction  : {time.perf_counter()-t:.2f}s")

            # =====================================================
            # VENDOR DETECTION
            # =====================================================

            t = time.perf_counter()
            vendor = VendorDetector.detect(
                text
            )
            print(f"Vendor Parser     : {time.perf_counter()-t:.2f}s")

            print(f"Detected Vendor   : {vendor}")

            # =====================================================
            # CHECK IF LLM NEEDED
            # =====================================================

            has_required = all(
                parsed_fields.get(f) not in [None, "", []]
                for f in ["invoice_number", "vendor_name", "invoice_date", "total"]
            )

            if has_required:

                invoice = parsed_fields
                print(f"LLM               : SKIPPED (required fields present)")

            else:

                t = time.perf_counter()
                extractor = ExtractorFactory.get(
                    vendor
                )

                invoice = extractor.extract(
                    text=text,
                    vendor=vendor,
                    parsed=parsed_fields,
                    items=items
                )
                print(f"Prompt Build + LLM  : {time.perf_counter()-t:.2f}s")

            # =====================================================
            # SAFETY
            # =====================================================

            if invoice is None:

                invoice = {}

            if not isinstance(invoice, dict):

                raise Exception(
                    "Extractor returned invalid invoice."
                )

            # =====================================================
            # VALIDATION
            # =====================================================

            t = time.perf_counter()
            result = InvoiceValidator.validate(
                invoice
            )
            print(f"Validation        : {time.perf_counter()-t:.2f}s")

            # =====================================================
            # CONFIDENCE
            # =====================================================

            t = time.perf_counter()
            confidence = ConfidenceScorer.calculate(
                result
            )
            print(f"Confidence        : {time.perf_counter()-t:.2f}s")

            result.update(
                confidence
            )

            # =====================================================
            # EXTRA INFORMATION
            # =====================================================

            result["vendor"] = vendor

            result["file_type"] = file_type

            # Uncomment only while debugging

            # result["raw_text"] = text

            # result["parsed_fields"] = parsed_fields

            # result["detected_items"] = items   

            # =====================================================
            # EXPORT JSON
            # =====================================================

            exported_file = Exporter.export_json(
                result
            )

            result["output_file"] = exported_file

            # =====================================================
            # PERFORMANCE
            # =====================================================

            end = time.perf_counter()

            processing_time = round(
                end - start,
                2
            )

            print("\n========================================")
            print(" Invoice Processing Completed")
            print("========================================")
            print(f"Vendor           : {vendor}")
            print(f"File Type        : {file_type}")
            print(f"Total Time       : {processing_time:.2f} sec")
            print(f"Confidence       : {confidence['confidence']}%")
            print(f"JSON Saved       : {exported_file}")
            print("========================================\n")

            return result

        # =====================================================
        # ERROR HANDLING
        # =====================================================

        except Exception as e:

            traceback.print_exc()

            end = time.perf_counter()

            processing_time = round(
                end - start,
                2
            )

            print("\n========================================")
            print(" Invoice Processing Failed")
            print("========================================")
            print(f"Error            : {str(e)}")
            print(f"Total Time       : {processing_time:.2f} sec")
            print("========================================\n")

            raise