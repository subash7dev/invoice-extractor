import re


def clean_text(text: str) -> str:
    """
    Clean OCR output before sending it to the LLM.
    """

    if not text:
        return ""

    # Normalize newlines
    text = text.replace("\r", "\n")

    # Remove tabs
    text = text.replace("\t", " ")

    # Collapse multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Remove empty lines
    lines = [line.strip() for line in text.split("\n")]
    lines = [line for line in lines if line]

    cleaned = []

    i = 0

    while i < len(lines):
        line = lines[i]

        # Merge wrapped invoice labels
        if (
            line.lower().startswith("invoice")
            and i + 1 < len(lines)
            and len(lines[i + 1]) < 20
        ):
            line += " " + lines[i + 1]
            i += 1

        cleaned.append(line)
        i += 1

    return "\n".join(cleaned)