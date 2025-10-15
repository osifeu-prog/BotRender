import logging

class DebugConfig:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("SELA")

    def log_bot_start(self):
        self.logger.info("🤖 SELA Bot Starting...")

    def log_error(self, where, e):
        self.logger.error(f"[{where}] {e}")

    def log_user_interaction(self, user_id, action):
        self.logger.info(f"👤 {user_id}: {action}")
