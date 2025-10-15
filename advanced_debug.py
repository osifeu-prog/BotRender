import logging
import os
import sys
from datetime import datetime

class AdvancedDebug:
    def __init__(self):
        self.setup_logging()
        self.start_time = datetime.now()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('bot_debug.log')
            ]
        )
        self.logger = logging.getLogger("SELA_Advanced")
        
    def log_system_info(self):
        self.logger.info("🤖 SELA Bot Starting - Advanced Debug Mode")
        self.logger.info(f"🖥️ Python: {sys.version}")
        self.logger.info(f"📁 Working Directory: {os.getcwd()}")
        self.logger.info(f"📦 Files in directory: {[f for f in os.listdir('.') if f.endswith('.py')]}")
        
        # Check environment variables (masked)
        env_vars = ["BOT_TOKEN", "ENCRYPTION_KEY", "ADMIN_ID", "BSC_RPC_URL"]
        for var in env_vars:
            value = os.getenv(var)
            if value:
                self.logger.info(f"🔑 {var}: {'*' * 10}{value[-4:] if len(value) > 4 else '***'}")
            else:
                self.logger.warning(f"❌ {var}: NOT SET")
    
    def log_database_status(self):
        db_files = ["wallets.db", "nfts.db", "rewards.db", "distribution.db"]
        for db_file in db_files:
            if os.path.exists(db_file):
                size = os.path.getsize(db_file)
                self.logger.info(f"🗃️ {db_file}: {size} bytes")
            else:
                self.logger.info(f"📝 {db_file}: Will be created on first run")
    
    def log_import_status(self):
        modules = [
            "telegram", "web3", "cryptography", "sqlite3", 
            "aiohttp", "PIL", "uvicorn", "fastapi"
        ]
        
        for module in modules:
            try:
                if module == "PIL":
                    __import__("PIL.Image")
                else:
                    __import__(module)
                self.logger.info(f"✅ {module}: Import successful")
            except ImportError as e:
                self.logger.error(f"❌ {module}: Import failed - {e}")
    
    def log_bot_ready(self):
        self.logger.info("🎉 Bot initialization completed successfully!")
        self.logger.info("📡 Starting polling...")

debug = AdvancedDebug()
