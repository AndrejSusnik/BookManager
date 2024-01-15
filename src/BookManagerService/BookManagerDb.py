import psycopg2
from config_managment import CustomConfigManager
import logging
import time

class BookManagerDb:
    def __init__(self, config_manager: CustomConfigManager, max_connection_attempts: int=5, connection_attempt_delay: int=5):
        host = config_manager.get("DB_URL", default="localhost")
        db_name = config_manager.get("DB_NAME", default="postgres")
        username = config_manager.get("DB_USER", default="postgres")
        password = config_manager.get("DB_PASSWORD", default="postgres")

        self.has_error = False

        while max_connection_attempts > 0:
            try:
                logging.info("Connecting to database %s on %s as %s", db_name, host, username)
                self.connection = psycopg2.connect(host=host, database=db_name, user=username, password=password)
                break
            except Exception as e:
                logging.error("Error while connecting to database: %s", str(e))
                max_connection_attempts -= 1
                if max_connection_attempts == 0:
                    self.has_error = True
                time.sleep(connection_attempt_delay)

    def __del__(self):
        self.connection.close()

    def get_cursor(self):
        return self.connection.cursor()