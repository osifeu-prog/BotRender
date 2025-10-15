import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.BOT_TOKEN = os.getenv('BOT_TOKEN')
        if not self.BOT_TOKEN:
            raise ValueError("❌ BOT_TOKEN is required in environment variables")
            
        self.ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))

        # Blockchain settings
        self.BSC_RPC_URL = "https://bsc-dataseed.binance.org/"
        self.CHAIN_ID = 56
        self.CONTRACT_ADDRESS = "0xACb0A09414CEA1C879c67bB7A877E4e19480f022"
        self.BSCSCAN_URL = "https://bscscan.com"

        # SELA settings
        self.SELA_PRICE_ILS = 244

        # Security - MUST be set in environment
        self.ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
        if not self.ENCRYPTION_KEY:
            raise ValueError("❌ ENCRYPTION_KEY is required in environment variables")

        # AI APIs
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
        self.HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN', '')

        # Reward settings
        self.REGISTRATION_REWARD = 0.44  # SELA for new users
        self.WALLET_CONNECT_REWARD = 1.0  # SELA for connecting external wallet

        # Web service
        self.WEB_SERVICE_URL = os.getenv('RENDER_EXTERNAL_URL', '')

        # Database paths
        self.DATABASE_PATH = 'wallets.db'
        self.NFT_DATABASE_PATH = 'nfts.db'
        self.DISTRIBUTION_DATABASE_PATH = 'distribution.db'
        self.REWARDS_DATABASE_PATH = 'rewards.db'

        # Cache settings
        self.CACHE_TIMEOUT = 300  # 5 minutes
        self.MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

        # Support
        self.SUPPORT_USERNAME = "@SELA_Support"
        self.COMMUNITY_LINK = "https://t.me/SELA_Community"

        # Security settings
        self.PRIVATE_KEY_CHECK = True
        self.ALLOW_EXTERNAL_WALLETS = True

        # Broadcast settings
        self.BROADCAST_DELAY = 0.1  # delay between broadcast messages
