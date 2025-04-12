from ifireflylib import IFireflyClient as FireflyDatabase
from .config import FIREFLY_HOST, FIREFLY_PORT, FIREFLY_PASSWORD
from .logger import logger

class DatabaseClient:
    @staticmethod
    def create_client():
        try:
            return FireflyDatabase(
                host=FIREFLY_HOST,
                port=FIREFLY_PORT,
                password=FIREFLY_PASSWORD,
            )
        except Exception as e:
            logger.error(f"Failed to create Firefly client: {e}")
            return None

    @staticmethod
    def get_key_type(client, key):
        try:
            type_result = client.execute_command("TYPE", key)
            if type_result and isinstance(type_result, str):
                if type_result.startswith(('+', '-', ':', '$', '*')):
                    type_result = type_result[1:]
                return type_result.strip().lower()
            return None
        except Exception as e:
            logger.debug(f"TYPE command failed for {key}: {e}")
            return None