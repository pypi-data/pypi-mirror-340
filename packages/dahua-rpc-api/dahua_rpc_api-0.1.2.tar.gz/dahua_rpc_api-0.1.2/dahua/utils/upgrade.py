from time import sleep
from dataclasses import dataclass

from dahua.client import DahuaRpc
from dahua.utils.logger import logger


@dataclass
class Upgrade:
    client: "DahuaRpc"

    def upgrade(self, firmware_path: str) -> bool:
        """Upgrade the firmware of the device."""
        logger.info("Starting firmware upgrade...")

        # Upload the firmware
        logger.info("Uploading firmware")
        if not self._upload_firmware(firmware_path):
            logger.error("Failed to upload firmware.")
            return False

        # Check upgrade progress
        if not self._check_progress():
            logger.error("Upgrade failed")
            return False

        logger.info("Firmware upgrade completed successfully.")
        return True

    def _upload_firmware(self, firmware_path: str) -> bool:
        cookies = {"DWebClientSessionID": self.client.session_id}

        with open(firmware_path, "rb") as f:
            files = {"fileupload": f}
            self.client.request_id += 1
            response = self.client.session.post(
                f"{self.client.base_url}/RPC2_Upgrade", files=files, cookies=cookies
            )

            return "sonia upgrade successfully" in response.text

    def _check_progress(self) -> bool:
        state = "Upgrading"

        while state == "Upgrading":
            update = self.client.upgrader.get_state()
            state = update.get("State")

            logger.info(f"Upgrade progress: {update.get('Progress')}%")
            logger.debug(f"Upgrade state: {update}")
            sleep(5)

        logger.debug(update)
        return state != "Invalid"
