import sqlite3, hashlib
from datetime import datetime

class NFTManager:
    def __init__(self):
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect('nfts.db')
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS user_nfts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                token_id TEXT,
                name TEXT,
                description TEXT,
                rarity INTEGER,
                created_at TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def _gen_id(self, user_id, name):
        s = f"{user_id}-{name}-{datetime.utcnow().timestamp()}".encode()
        return hashlib.sha256(s).hexdigest()[:16]

    def get_user_nfts(self, user_id):
        conn = sqlite3.connect('nfts.db')
        cur = conn.cursor()
        cur.execute("SELECT token_id, name, description, rarity, created_at FROM user_nfts WHERE user_id=?",
                    (user_id,))
        rows = cur.fetchall()
        conn.close()
        res = []
        for r in rows:
            res.append({
                "token_id": r[0], "name": r[1], "description": r[2],
                "rarity": r[3], "created_at": r[4]
            })
        return res

    def award_nft(self, user_id, nft_type, purchase_id=None):
        name_map = {
            "starter": "SELA Starter NFT 🌟",
            "elite": "SELA Elite NFT 💎",
            "founder": "SELA Founder NFT 🚀",
            "whale": "SELA Whale NFT 🔥",
            "royal": "SELA Royal NFT 👑",
        }
        name = name_map.get(nft_type, "SELA NFT")
        token_id = self._gen_id(user_id, name)
        conn = sqlite3.connect('nfts.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO user_nfts(user_id, token_id, name, description, rarity, created_at) VALUES(?,?,?,?,?,?)",
                    (user_id, token_id, name, f"Awarded for purchase {purchase_id}", 3, datetime.now()))
        conn.commit()
        conn.close()
        return {"success": True, "token_id": token_id, "name": name}

    def create_custom_nft(self, user_id, name, description, image, rarity):
        token_id = self._gen_id(user_id, name)
        conn = sqlite3.connect('nfts.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO user_nfts(user_id, token_id, name, description, rarity, created_at) VALUES(?,?,?,?,?,?)",
                    (user_id, token_id, name, description, int(rarity), datetime.now()))
        conn.commit()
        conn.close()
        return {"success": True, "token_id": token_id}
