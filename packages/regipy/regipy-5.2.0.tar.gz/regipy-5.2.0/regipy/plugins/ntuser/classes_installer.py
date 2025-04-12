import logging

from regipy import RegistryKeyNotFoundException, convert_wintime
from regipy.hive_types import NTUSER_HIVE_TYPE
from regipy.plugins.plugin import Plugin

logger = logging.getLogger(__name__)

CLASSES_INSTALLER_PATH = r"\Software\Microsoft\Installer\Products"


class NtuserClassesInstallerPlugin(Plugin):
    NAME = "ntuser_classes_installer"
    DESCRIPTION = "List of installed software from NTUSER hive"
    COMPATIBLE_HIVE = NTUSER_HIVE_TYPE

    def run(self):
        try:
            classes_installer_subkey = self.registry_hive.get_key(
                CLASSES_INSTALLER_PATH
            )
        except RegistryKeyNotFoundException as ex:
            logger.error(ex)
            return

        for entry in classes_installer_subkey.iter_subkeys():
            identifier = entry.name
            timestamp = convert_wintime(
                entry.header.last_modified, as_json=self.as_json
            )
            product_name = entry.get_value("ProductName")
            self.entries.append(
                {
                    "identifier": identifier,
                    "timestamp": timestamp,
                    "product_name": product_name,
                    "is_hidden": product_name is None,
                }
            )
