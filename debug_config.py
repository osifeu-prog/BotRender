import logging
import time
from datetime import datetime

class DebugConfig:
    def __init__(self):
        self.start_time = time.time()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

    def log_bot_start(self):
        logging.info("🤖 SELA Bot Starting...")
        logging.info(f"⏰ Start Time: {datetime.now()}")

    def log_user_interaction(self, user_id: int, action: str):
        logging.info(f"👤 User {user_id} - Action: {action}")

    def log_error(self, context: str, error: Exception):
        logging.error(f"❌ Error in {context}: {error}")

    def log_database_operation(self, operation: str, table: str):
        logging.info(f"🗃️ DB {operation} on {table}")

    def log_blockchain_interaction(self, action: str, address: str = ""):
        logging.info(f"⛓️ Blockchain {action} {address}")

    def get_uptime(self):
        return time.time() - self.start_time

    def log_bot_stop(self):
        uptime = self.get_uptime()
        logging.info(f"🛑 Bot Stopped - Uptime: {uptime:.2f} seconds")
