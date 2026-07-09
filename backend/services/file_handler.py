from pathlib import Path
import mimetypes


class FileHandler:
    """
    Handles file validation and metadata.
    """

    IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".tiff",
        ".tif",
        ".webp"
    }

    PDF_EXTENSIONS = {
        ".pdf"
    }

    ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | PDF_EXTENSIONS

    @staticmethod
    def exists(file_path: str) -> bool:
        """
        Check whether the file exists.
        """
        return Path(file_path).exists()

    @staticmethod
    def get_extension(file_path: str) -> str:
        """
        Return file extension.
        """
        return Path(file_path).suffix.lower()

    @staticmethod
    def get_filename(file_path: str) -> str:
        """
        Return filename.
        """
        return Path(file_path).name

    @staticmethod
    def get_size(file_path: str) -> int:
        """
        Return file size in bytes.
        """
        return Path(file_path).stat().st_size

    @staticmethod
    def is_empty(file_path: str) -> bool:
        """
        Check whether file is empty.
        """
        return FileHandler.get_size(file_path) == 0

    @staticmethod
    def get_mime_type(file_path: str) -> str:
        """
        Detect MIME type.
        """
        mime_type, _ = mimetypes.guess_type(file_path)

        return mime_type or "application/octet-stream"

    @staticmethod
    def get_file_type(file_path: str) -> str:
        """
        Returns:
            image
            pdf

        Raises:
            ValueError if unsupported.
        """

        suffix = FileHandler.get_extension(file_path)

        if suffix in FileHandler.IMAGE_EXTENSIONS:
            return "image"

        if suffix in FileHandler.PDF_EXTENSIONS:
            return "pdf"

        raise ValueError(
            f"Unsupported file type: {suffix}"
        )

    @staticmethod
    def validate(file_path: str):
        """
        Validate uploaded file.
        """

        if not FileHandler.exists(file_path):
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if FileHandler.is_empty(file_path):
            raise ValueError(
                "Uploaded file is empty."
            )

        suffix = FileHandler.get_extension(file_path)

        if suffix not in FileHandler.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {suffix}"
            )

        return True

    @staticmethod
    def info(file_path: str):
        """
        Return file metadata.
        """

        return {

            "filename": FileHandler.get_filename(file_path),

            "extension": FileHandler.get_extension(file_path),

            "mime_type": FileHandler.get_mime_type(file_path),

            "size_bytes": FileHandler.get_size(file_path),

            "type": FileHandler.get_file_type(file_path)
        }