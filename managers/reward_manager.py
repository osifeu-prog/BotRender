import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RewardManager:
    def __init__(self, bot=None):  # הוסף פרמטר bot
        self.bot = bot
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect('rewards.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_rewards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                reward_type TEXT,
                amount REAL,
                description TEXT,
                awarded_at TIMESTAMP,
                is_claimed BOOLEAN DEFAULT FALSE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reward_claims (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                reward_id INTEGER,
                claimed_at TIMESTAMP,
                transaction_hash TEXT,
                FOREIGN KEY (reward_id) REFERENCES user_rewards (id)
            )
        ''')

        conn.commit()
        conn.close()

    def award_registration_bonus(self, user_id):
        """מתנת הרשמה - 0.44 SELA"""
        try:
            if hasattr(self, 'bot') and self.bot:
                amount = self.bot.config.REGISTRATION_REWARD
            else:
                amount = 0.44

            conn = sqlite3.connect('rewards.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id FROM user_rewards 
                WHERE user_id = ? AND reward_type = 'registration'
            ''', (user_id,))

            if cursor.fetchone():
                conn.close()
                return {'success': False, 'error': 'Reward already awarded'}

            cursor.execute('''
                INSERT INTO user_rewards 
                (user_id, reward_type, amount, description, awarded_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, 'registration', amount, 'מתנת הרשמה לקהילת SELA', datetime.now()))

            conn.commit()
            conn.close()

            logger.info(f"✅ Registration bonus awarded to user {user_id}: {amount} SELA")
            return {'success': True, 'amount': amount}

        except Exception as e:
            logger.error(f"❌ Error awarding registration bonus: {e}")
            return {'success': False, 'error': str(e)}

    def award_wallet_creation(self, user_id):
        """מתנה על יצירת ארנק"""
        try:
            if hasattr(self, 'bot') and self.bot:
                amount = self.bot.config.WALLET_CONNECT_REWARD
            else:
                amount = 1.0

            conn = sqlite3.connect('rewards.db')
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO user_rewards 
                (user_id, reward_type, amount, description, awarded_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, 'wallet_creation', amount, 'מתנה על יצירת ארנק SELA', datetime.now()))

            conn.commit()
            conn.close()

            logger.info(f"✅ Wallet creation bonus awarded to user {user_id}: {amount} SELA")
            return {'success': True, 'amount': amount}

        except Exception as e:
            logger.error(f"❌ Error awarding wallet creation bonus: {e}")
            return {'success': False, 'error': str(e)}

    def award_wallet_connection(self, user_id):
        """מתנה על חיבור ארנק חיצוני"""
        try:
            if hasattr(self, 'bot') and self.bot:
                amount = self.bot.config.WALLET_CONNECT_REWARD
            else:
                amount = 1.0

            conn = sqlite3.connect('rewards.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id FROM user_rewards 
                WHERE user_id = ? AND reward_type = 'wallet_connection'
            ''', (user_id,))

            if cursor.fetchone():
                conn.close()
                return {'success': False, 'error': 'Connection reward already awarded'}

            cursor.execute('''
                INSERT INTO user_rewards 
                (user_id, reward_type, amount, description, awarded_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, 'wallet_connection', amount, 'מתנה על חיבור ארנק חיצוני', datetime.now()))

            conn.commit()
            conn.close()

            logger.info(f"✅ Wallet connection bonus awarded to user {user_id}: {amount} SELA")
            return {'success': True, 'amount': amount}

        except Exception as e:
            logger.error(f"❌ Error awarding wallet connection: {e}")
            return {'success': False, 'error': str(e)}

    def get_user_rewards(self, user_id):
        """קבלת כל המתנות של משתמש"""
        try:
            conn = sqlite3.connect('rewards.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT reward_type, amount, description, awarded_at, is_claimed
                FROM user_rewards 
                WHERE user_id = ?
                ORDER BY awarded_at DESC
            ''', (user_id,))

            rewards = []
            total_claimed = 0
            total_pending = 0

            for row in cursor.fetchall():
                reward = {
                    'type': row[0],
                    'amount': row[1],
                    'description': row[2],
                    'awarded_at': row[3],
                    'is_claimed': row[4]
                }
                rewards.append(reward)

                if row[4]:
                    total_claimed += row[1]
                else:
                    total_pending += row[1]

            conn.close()

            return {
                'success': True,
                'rewards': rewards,
                'total_claimed': total_claimed,
                'total_pending': total_pending,
                'total_all': total_claimed + total_pending
            }

        except Exception as e:
            logger.error(f"❌ Error getting user rewards: {e}")
            return {'success': False, 'error': str(e)}
