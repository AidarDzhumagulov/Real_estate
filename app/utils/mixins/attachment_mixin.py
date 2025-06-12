import os
from abc import abstractmethod
from typing import Dict, Iterable, List, Tuple

from app.utils.logging import logger


class CreateAttachmentMixin:

    def _create_attachment(self, file_hash, relative_path, filename, extension, mime, size):
        """Creates attachment in the database."""
        return "attachment"
