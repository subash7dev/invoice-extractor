import json
import os
import re
import time

import ollama
from dotenv import load_dotenv

from services.prompt_builder import PromptBuilder

load_dotenv()


class LLMService:
    """
    Production-grade LLM service.
    """

    MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

    @classmethod
    def extract(
        cls,
        text: str,
        vendor: str,
        detected_items=None,
        parsed_fields=None
    ):
        parsed_fields = parsed_fields or {}
        detected_items = detected_items or []

        prompt = PromptBuilder.build(text, vendor, parsed_fields, detected_items)
        start_time = time.time()

        try:
            response = ollama.chat(
                model=cls.MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0,
                    "num_predict": 256,
                    "num_ctx": 4096
                }
            )
            PromptBuilder.log_stats(prompt, start_time)

            content = response["message"]["content"]
            parsed = cls.parse_json(content)

            if parsed:
                return cls.merge(
                    parsed,
                    parsed_fields,
                    detected_items
                )

        except Exception as e:
            print("LLM Error:", e)

        return cls.merge(
            {},
            parsed_fields,
            detected_items
        )

    @staticmethod
    def parse_json(response):
        if not response:
            return None

        response = response.replace(
            "```json",
            ""
        )

        response = response.replace(
            "```",
            ""
        )

        response = response.strip()

        try:
            return json.loads(response)
        except Exception:
            pass

        match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL
        )

        if match:
            try:
                return json.loads(
                    match.group()
                )
            except Exception:
                pass

        return None

    @staticmethod
    def merge(
        llm_result,
        parser_result,
        items
    ):
        result = llm_result.copy()

        for key, value in parser_result.items():
            if value not in [
                None,
                "",
                []
            ]:
                if result.get(key) in [
                    None,
                    "",
                    []
                ]:
                    result[key] = value

        if items:
            if not result.get("items"):
                result["items"] = items

        return result