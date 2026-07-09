from pathlib import Path


class PromptManager:
    """
    Loads vendor-specific prompts.

    Priority:
        1. prompts/<vendor>.txt
        2. prompts/generic.txt
    """

    PROMPT_DIR = Path("prompts")

    DEFAULT_PROMPT = "generic.txt"

    @classmethod
    def load_prompt(cls, vendor: str) -> str:

        if not vendor:
            vendor = "generic"

        vendor = vendor.lower().strip()

        prompt_file = cls.PROMPT_DIR / f"{vendor}.txt"

        if prompt_file.exists():

            return prompt_file.read_text(
                encoding="utf-8"
            )

        default_prompt = cls.PROMPT_DIR / cls.DEFAULT_PROMPT

        if default_prompt.exists():

            return default_prompt.read_text(
                encoding="utf-8"
            )

        raise FileNotFoundError(
            "No prompt file found."
        )

    @classmethod
    def available_prompts(cls):

        if not cls.PROMPT_DIR.exists():

            return []

        return sorted(

            [

                file.stem

                for file in cls.PROMPT_DIR.glob("*.txt")

            ]

        )

    @classmethod
    def exists(cls, vendor: str) -> bool:

        vendor = vendor.lower().strip()

        return (

            cls.PROMPT_DIR / f"{vendor}.txt"

        ).exists()

    @classmethod
    def reload(cls):

        """
        Placeholder for future caching support.
        """
        return True