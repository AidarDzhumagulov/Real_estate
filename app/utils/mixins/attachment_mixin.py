import os
from abc import abstractmethod
from typing import Dict, Iterable, List, Tuple

from app.utils.excel_writer import ExcelWriter, WorkSheetConfig
from app.utils.file_util import FileUtil
from app.utils.logging import logger


class CreateAttachmentMixin:
    SYSTEM_USER_ID = 1

    # TODO(aidar): Нужно сделать таблицу для attachment

    def _create_attachment(self, file_hash, relative_path, filename, extension, mime, size):
        """Creates attachment in the database."""
        return "attachment"


class ExcelAttachmentMixin(CreateAttachmentMixin):
    # TODO(aidar): Этот класс тоже буду переделывать под нашу систему
    @abstractmethod
    async def excel_writer_data(self) -> Tuple[str, Dict[WorkSheetConfig, List[Iterable]]]:
        pass

    def create_workbook(self, filename, sheets_data: Dict[WorkSheetConfig, List[Iterable]]):
        try:
            with ExcelWriter(filename, list(sheets_data.keys())) as excel_writer:
                excel_writer.write_worksheets(sheets_data)
                absolute_path = excel_writer.absolute_path
                extension = excel_writer.extension
                mime = excel_writer.mime

            file_hash, abs_path, rel_path = FileUtil.get_new_file_path(
                path=absolute_path, extension=extension
            )
            file_size = FileUtil.filesize(os.path.getsize(abs_path))

            attachment = self._create_attachment(
                file_hash, rel_path, filename, extension, mime, file_size
            )
        except BaseException as e:
            logger.error(e)
            raise

        return attachment

    async def create_report(self):
        """Создание отчета в xlsx файле"""
        registry_attachment = self.create_workbook(*(await self.excel_writer_data()))
        return registry_attachment
