import logging
import sqlite3
import json
from web3 import Web3
import os

logger = logging.getLogger(__name__)

class WalletManager:
    def __init__(self, config):
        self.config = config
        self.w3 = Web3(Web3.HTTPProvider(config.BSC_RPC_URL))
        self.init_database()

    def init_database(self):
        """אתחול מסד הנתונים של ארנקים"""
        try:
            conn = sqlite3.connect(self.config.DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS wallets (
                    user_id INTEGER PRIMARY KEY,
                    wallet_address TEXT UNIQUE,
                    private_key_encrypted TEXT,
                    balance REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    tx_hash TEXT,
                    amount REAL,
                    tx_type TEXT,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES wallets (user_id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ Wallet database initialized")
            
        except Exception as e:
            logger.error(f"❌ Error initializing wallet database: {e}")

    def create_wallet(self, user_id):
        """יצירת ארנק חדש למשתמש"""
        try:
            # יצירת ארנק חדש (בסביבה אמיתית - השתמש ב-web3)
            account = self.w3.eth.account.create()
            wallet_address = account.address
            private_key = account.key.hex()
            
            # כאן יש להצפין את המפתח הפרטי לפני השמירה
            private_key_encrypted = private_key  # בחלק זה יש להשתמש בהצפנה
            
            conn = sqlite3.connect(self.config.DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO wallets (user_id, wallet_address, private_key_encrypted)
                VALUES (?, ?, ?)
            ''', (user_id, wallet_address, private_key_encrypted))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Wallet created for user {user_id}")
            return wallet_address
            
        except Exception as e:
            logger.error(f"❌ Error creating wallet: {e}")
            return None

    def get_wallet(self, user_id):
        """קבלת פרטי ארנק משתמש"""
        try:
            conn = sqlite3.connect(self.config.DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT wallet_address, balance FROM wallets WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'address': result[0],
                    'balance': result[1]
                }
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting wallet: {e}")
            return None

    def get_balance(self, wallet_address):
        """קבלת יתוך מהבלוקצ'יין"""
        try:
            balance_wei = self.w3.eth.get_balance(wallet_address)
            balance_bnb = self.w3.from_wei(balance_wei, 'ether')
            return float(balance_bnb)
        except Exception as e:
            logger.error(f"❌ Error getting balance: {e}")
            return 0.0

    def update_balance(self, user_id):
        """עדכון יתוך במסד הנתונים"""
        try:
            wallet = self.get_wallet(user_id)
            if wallet:
                current_balance = self.get_balance(wallet['address'])
                
                conn = sqlite3.connect(self.config.DATABASE_PATH)
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE wallets SET balance = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (current_balance, user_id))
                
                conn.commit()
                conn.close()
                return current_balance
            return 0.0
            
        except Exception as e:
            logger.error(f"❌ Error updating balance: {e}")
            return 0.0

    def add_transaction(self, user_id, tx_hash, amount, tx_type, status="pending"):
        """הוספת עסקה למסד הנתונים"""
        try:
            conn = sqlite3.connect(self.config.DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO transactions (user_id, tx_hash, amount, tx_type, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, tx_hash, amount, tx_type, status))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ Error adding transaction: {e}")
            return False

    def get_transactions(self, user_id, limit=10):
        """קבלת היסטוריית עסקות"""
        try:
            conn = sqlite3.connect(self.config.DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT tx_hash, amount, tx_type, status, created_at
                FROM transactions 
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            
            transactions = cursor.fetchall()
            conn.close()
            
            return [{
                'tx_hash': tx[0],
                'amount': tx[1],
                'type': tx[2],
                'status': tx[3],
                'timestamp': tx[4]
            } for tx in transactions]
            
        except Exception as e:
            logger.error(f"❌ Error getting transactions: {e}")
            return []
