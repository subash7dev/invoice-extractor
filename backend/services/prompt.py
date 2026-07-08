from pathlib import Path

PROMPT_TEMPLATE = Path("prompts/invoice_prompt.txt").read_text(
    encoding="utf-8"
)


def build_prompt(ocr_text: str) -> str:
    """
    Build the final prompt sent to the LLM.
    """

    return f"""
{PROMPT_TEMPLATE}

==========================
OCR TEXT
==========================

{ocr_text}

==========================
Return ONLY valid JSON.
"""