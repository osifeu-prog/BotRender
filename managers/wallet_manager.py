import sqlite3
from datetime import datetime
import secrets

class WalletManager:
    def __init__(self, config):
        self.config = config
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect('wallets.db')
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS user_wallets(
                user_id INTEGER PRIMARY KEY,
                public_address TEXT,
                private_key TEXT,
                created_at TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def create_wallet(self, user_id):
        # dummy wallet (for demo); replace with real web3 logic if needed
        pub = "0x" + secrets.token_hex(20)
        prv = secrets.token_hex(32)
        conn = sqlite3.connect('wallets.db')
        cur = conn.cursor()
        cur.execute("REPLACE INTO user_wallets(user_id, public_address, private_key, created_at) VALUES(?,?,?,?)",
                    (user_id, pub, prv, datetime.now()))
        conn.commit()
        conn.close()
        return {
            "success": True,
            "public_address": pub,
            "created_date": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

    def get_wallet(self, user_id):
        conn = sqlite3.connect('wallets.db')
        cur = conn.cursor()
        cur.execute("SELECT public_address, created_at FROM user_wallets WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return {"public_address": row[0], "created_date": row[1]}
