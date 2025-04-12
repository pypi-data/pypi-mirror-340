import logging

from regipy.exceptions import RegistryKeyNotFoundException
from regipy.hive_types import NTUSER_HIVE_TYPE
from regipy.plugins.plugin import Plugin
from regipy.utils import convert_wintime

logger = logging.getLogger(__name__)

WINRAR_ARCHIVE_CREATION_HIST = r"\SOFTWARE\WinRAR\DialogEditHistory\ArcName"
WINRAR_ARCHIVE_EXTRACT_HIST = r"\SOFTWARE\WinRAR\DialogEditHistory\ExtrPath"
WINRAR_ARCHIVE_OPEN_HIST = r"\SOFTWARE\WinRAR\ArcHistory"


class WinRARPlugin(Plugin):
    NAME = "winrar_plugin"
    DESCRIPTION = "Parse the WinRAR archive history"
    COMPATIBLE_HIVE = NTUSER_HIVE_TYPE

    def run(self):
        try:
            open_subkey = self.registry_hive.get_key(WINRAR_ARCHIVE_OPEN_HIST)

            timestamp = convert_wintime(
                open_subkey.header.last_modified, as_json=self.as_json
            )
            for value in open_subkey.iter_values(as_json=self.as_json):
                self.entries.append(
                    {
                        "last_write": timestamp,
                        "file_path": value.value,
                        "value_name": value.name,
                        "operation": "archive_opened",
                    }
                )

        except RegistryKeyNotFoundException as ex:
            logger.error(
                f"Could not find {self.NAME} plugin data at: {WINRAR_ARCHIVE_OPEN_HIST}: {ex}"
            )

        try:
            create_subkey = self.registry_hive.get_key(WINRAR_ARCHIVE_CREATION_HIST)

            timestamp = convert_wintime(
                create_subkey.header.last_modified, as_json=self.as_json
            )
            for value in create_subkey.iter_values(as_json=self.as_json):
                self.entries.append(
                    {
                        "last_write": timestamp,
                        "file_name": value.value,
                        "value_name": value.name,
                        "operation": "archive_created",
                    }
                )

        except RegistryKeyNotFoundException as ex:
            logger.error(
                f"Could not find {self.NAME} plugin data at: {WINRAR_ARCHIVE_CREATION_HIST}: {ex}"
            )

        try:
            extract_subkey = self.registry_hive.get_key(WINRAR_ARCHIVE_EXTRACT_HIST)

            timestamp = convert_wintime(
                extract_subkey.header.last_modified, as_json=self.as_json
            )
            for value in extract_subkey.iter_values(as_json=self.as_json):
                self.entries.append(
                    {
                        "last_write": timestamp,
                        "file_path": value.value,
                        "value_name": value.name,
                        "operation": "archive_extracted",
                    }
                )

        except RegistryKeyNotFoundException as ex:
            logger.error(
                f"Could not find {self.NAME} plugin data at: {WINRAR_ARCHIVE_EXTRACT_HIST}: {ex}"
            )
