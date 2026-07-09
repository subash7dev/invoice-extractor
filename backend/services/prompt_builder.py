import json
import re


class PromptBuilder:
    """
    Generates compact LLM prompts for invoice extraction.
    """

    MAX_PROMPT_CHARS = 4000

    @staticmethod
    def build(text: str, vendor: str, parsed_fields: dict, detected_items: list) -> str:
        """
        Build a compact prompt under 4000 characters.
        Includes only essential fields, removes empty values and duplicates.
        """
        # Clean and extract relevant fields from OCR text
        clean_text = PromptBuilder._clean_text(text)
        
        # Extract only relevant fields from parsed_fields
        relevant = PromptBuilder._filter_relevant_fields(parsed_fields)
        
        # Build prompt
        parts = []
        
        # Invoice header
        parts.append("Extract invoice fields. Return ONLY valid JSON.")
        
        # Vendor
        if vendor:
            parts.append(f"Vendor: {vendor}")
        
        # Customer
        if relevant.get("customer"):
            parts.append(f"Customer: {relevant['customer']}")
        
        # Invoice number
        if relevant.get("invoice_number"):
            parts.append(f"Invoice #: {relevant['invoice_number']}")
        
        # Invoice date
        if relevant.get("invoice_date"):
            parts.append(f"Date: {relevant['invoice_date']}")
        
        # Due date
        if relevant.get("due_date"):
            parts.append(f"Due: {relevant['due_date']}")
        
        # Purchase order
        if relevant.get("purchase_order"):
            parts.append(f"PO: {relevant['purchase_order']}")
        
        # Totals
        for field in ["subtotal", "tax", "total", "shipping", "discount"]:
            if relevant.get(field) is not None:
                parts.append(f"{field.capitalize()}: {relevant[field]}")
        
        # Currency
        if relevant.get("currency"):
            parts.append(f"Currency: {relevant['currency']}")
        
        # Detected items (compact)
        if detected_items:
            parts.append(f"Items: {json.dumps(detected_items, separators=(',', ':'))}")
        
        # Parser output (compact)
        if relevant:
            parts.append(f"Parser: {json.dumps(relevant, separators=(',', ':'))}")
        
        # OCR text (truncated)
        ocr_part = PromptBuilder._truncate_ocr(clean_text)
        if ocr_part:
            parts.append(f"OCR: {ocr_part}")
        
        prompt = "\n".join(parts)
        
        # Ensure under limit
        if len(prompt) > PromptBuilder.MAX_PROMPT_CHARS:
            prompt = prompt[:PromptBuilder.MAX_PROMPT_CHARS]
        
        return prompt

    @staticmethod
    def _clean_text(text: str) -> str:
        """Remove repeated whitespace and clean text."""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    @staticmethod
    def _filter_relevant_fields(parsed_fields: dict) -> dict:
        """Keep only relevant fields, remove empty values."""
        relevant = {}
        fields = [
            "invoice_number", "vendor_name", "customer", "invoice_date",
            "due_date", "purchase_order", "subtotal", "tax", "total",
            "shipping", "discount", "currency"
        ]
        for field in fields:
            value = parsed_fields.get(field)
            if value not in [None, "", []]:
                relevant[field] = value
        return relevant

    @staticmethod
    def _truncate_ocr(text: str) -> str:
        """Truncate OCR text to keep prompt under limit."""
        # Reserve ~1000 chars for other fields
        max_ocr = PromptBuilder.MAX_PROMPT_CHARS - 1000
        if len(text) > max_ocr:
            return text[:max_ocr] + "..."
        return text

    @staticmethod
    def log_stats(prompt: str, start_time: float) -> None:
        """Log prompt length and inference time."""
        import time as time_module
        elapsed = time_module.time() - start_time
        print(f"Prompt length: {len(prompt)} chars, Inference time: {elapsed:.2f}s")
