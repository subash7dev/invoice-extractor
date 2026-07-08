from ollama import chat
from services.prompt import build_prompt


def extract_invoice(ocr_text: str):

    prompt = build_prompt(ocr_text)

    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]