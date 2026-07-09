import json
from datetime import datetime
from pathlib import Path


class Exporter:
    """
    Production-grade JSON exporter.
    """

    DEFAULT_OUTPUT_DIR = Path("outputs")

    @classmethod
    def export_json(

        cls,

        data: dict,

        filename: str | None = None,

        output_dir: str | None = None

    ) -> str:

        if output_dir is None:

            output_path = cls.DEFAULT_OUTPUT_DIR

        else:

            output_path = Path(output_dir)

        output_path.mkdir(

            parents=True,

            exist_ok=True

        )

        if filename is None:

            filename = (

                "invoice_"

                + datetime.now().strftime(

                    "%Y%m%d_%H%M%S"

                )

                + ".json"

            )

        file_path = output_path / filename

        with open(

            file_path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                data,

                file,

                indent=4,

                ensure_ascii=False

            )

        return str(file_path)

    @staticmethod
    def load_json(file_path: str):

        with open(

            file_path,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    @staticmethod
    def pretty(data: dict):

        return json.dumps(

            data,

            indent=4,

            ensure_ascii=False

        )