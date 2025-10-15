import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DistributionManager:
    def __init__(self, bot=None):  # הוסף פרמטר bot
        self.bot = bot
        self.sela_price_ils = 244
        self.init_database()

    def init_database(self):
        try:
            conn = sqlite3.connect('distribution.db')
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS purchases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    sela_amount REAL,
                    total_price_ils REAL,
                    payment_method TEXT,
                    status TEXT,
                    nft_awarded BOOLEAN DEFAULT FALSE,
                    nft_token_id TEXT,
                    nft_type TEXT,
                    created_at TIMESTAMP,
                    completed_at TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referrer_id INTEGER,
                    referred_id INTEGER,
                    reward_sela REAL DEFAULT 5.0,
                    is_claimed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    achievement_key TEXT,
                    unlocked_at TIMESTAMP,
                    reward_claimed BOOLEAN DEFAULT FALSE
                )
            ''')

            conn.commit()
            conn.close()
            logger.info("✅ Distribution database initialized successfully")
        except Exception as e:
            logger.error(f"❌ Distribution database initialization failed: {e}")

    def create_purchase_order(self, user_id, sela_amount, payment_method="bank_transfer"):
        try:
            total_price = sela_amount * self.sela_price_ils
            nft_type = self.get_nft_type_by_purchase(sela_amount)

            conn = sqlite3.connect('distribution.db')
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO purchases 
                (user_id, sela_amount, total_price_ils, payment_method, status, nft_type, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, sela_amount, total_price, payment_method, 'pending', nft_type, datetime.now()))

            purchase_id = cursor.lastrowid

            conn.commit()
            conn.close()

            logger.info(f"✅ Purchase order created for user {user_id}: {sela_amount} SELA")

            return {
                'purchase_id': purchase_id,
                'sela_amount': sela_amount,
                'total_price_ils': total_price,
                'nft_type': nft_type,
                'nft_name': self.get_nft_display_name(nft_type),
                'payment_instructions': self.get_payment_instructions(payment_method, total_price, purchase_id),
                'bonuses': self.calculate_bonuses(sela_amount)
            }

        except Exception as e:
            logger.error(f"❌ Error creating purchase order: {e}")
            return {'success': False, 'error': str(e)}

    def get_nft_type_by_purchase(self, sela_amount):
        if sela_amount >= 500: return "royal"
        elif sela_amount >= 250: return "whale"
        elif sela_amount >= 100: return "founder"
        elif sela_amount >= 50: return "elite"
        elif sela_amount >= 10: return "starter"
        return None

    def get_nft_display_name(self, nft_type):
        names = {
            "starter": "SELA Starter NFT 🌟",
            "elite": "SELA Elite NFT 💎", 
            "founder": "SELA Founder NFT 🚀",
            "whale": "SELA Whale NFT 🔥",
            "royal": "SELA Royal NFT 👑"
        }
        return names.get(nft_type, "SELA NFT")

    def calculate_bonuses(self, sela_amount):
        bonuses = []
        if sela_amount >= 500:
            bonuses.extend(["15% הנחה", "NFT בלעדי", "תואר יועץ", "קבוצת יועצים", "גישה לכל האירועים"])
        elif sela_amount >= 250:
            bonuses.extend(["12% הנחה", "NFT אגדי+", "תואר מייסד", "קבוצת מייסדים", "השפעה על החלטות"])
        elif sela_amount >= 100:
            bonuses.extend(["10% הנחה", "NFT אגדי", "תואר מייסד", "רווחים מועדפים", "קבוצת מייסדים"])
        elif sela_amount >= 50:
            bonuses.extend(["NFT נדיר", "תואר חבר קהילה", "זכות הצבעה"])
        elif sela_amount >= 10:
            bonuses.extend(["NFT בסיסי", "גישה לקהילה"])
        return bonuses

    def get_payment_instructions(self, method, amount, purchase_id):
        if method == "bank_transfer":
            return f"""
🏦 **הוראות העברה בנקאית:**

**בנק:** בנק דיגיטלי
**סניף:** 999
**מספר חשבון:** 1234567
**שם:** SELA Projects Ltd.

💸 **סכום להעברה:** {amount:,.0f} ₪
📝 **הערה:** SELA Purchase #{purchase_id}

✅ **לאחר ההעברה:**
1. שמור את אישור ההעברה
2. שלח אלינו את האישור
3. הקבל את ה-SELA וה-NFT שלך בתוך 24 שעות

📞 **תמיכה:** @SELA_Support
"""
        else:
            return "💳 **תשלום בכרטיס אשראי** - זמין בקרוב!"

    def process_referral(self, referrer_id, referred_id):
        try:
            conn = sqlite3.connect('distribution.db')
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO referrals (referrer_id, referred_id, created_at)
                VALUES (?, ?, ?)
            ''', (referrer_id, referred_id, datetime.now()))

            conn.commit()
            conn.close()

            logger.info(f"✅ Referral processed: {referrer_id} -> {referred_id}")

        except Exception as e:
            logger.error(f"❌ Error processing referral: {e}")

    def award_purchase_nft(self, user_id, purchase_id):
        try:
            conn = sqlite3.connect('distribution.db')
            cursor = conn.cursor()

            cursor.execute('SELECT nft_type FROM purchases WHERE id = ?', (purchase_id,))
            result = cursor.fetchone()

            if result:
                nft_type = result[0]
                # תיקון קריטי - שימוש ב-nft_manager הנכון
                if hasattr(self, 'bot') and self.bot:
                    nft_result = self.bot.nft_manager.award_nft(user_id, nft_type, purchase_id)
                else:
                    from managers.nft_manager import NFTManager
                    temp_nft_manager = NFTManager()
                    nft_result = temp_nft_manager.award_nft(user_id, nft_type, purchase_id)

                if nft_result['success']:
                    cursor.execute('''
                        UPDATE purchases 
                        SET nft_awarded = TRUE, nft_token_id = ?, status = 'completed', completed_at = ?
                        WHERE id = ?
                    ''', (nft_result['token_id'], datetime.now(), purchase_id))

                    conn.commit()
                    conn.close()

                    logger.info(f"✅ NFT awarded for purchase {purchase_id}: {nft_result['name']}")
                    return nft_result

            conn.close()
            return {'success': False, 'error': 'Purchase not found'}

        except Exception as e:
            logger.error(f"❌ Error awarding purchase NFT: {e}")
            return {'success': False, 'error': str(e)}

    def get_user_purchases(self, user_id):
        try:
            conn = sqlite3.connect('distribution.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, sela_amount, total_price_ils, status, nft_type, created_at
                FROM purchases WHERE user_id = ? ORDER BY created_at DESC
            ''', (user_id,))

            purchases = []
            for row in cursor.fetchall():
                purchases.append({
                    'id': row[0],
                    'sela_amount': row[1],
                    'total_price': row[2],
                    'status': row[3],
                    'nft_type': row[4],
                    'created_at': row[5]
                })

            conn.close()
            return purchases

        except Exception as e:
            logger.error(f"❌ Error getting user purchases: {e}")
            return []

    def get_referral_stats(self, user_id):
        try:
            conn = sqlite3.connect('distribution.db')
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM referrals WHERE referrer_id = ?', (user_id,))
            total_referred = cursor.fetchone()[0]

            cursor.execute('''
                SELECT COUNT(DISTINCT r.referred_id) 
                FROM referrals r
                JOIN purchases p ON r.referred_id = p.user_id 
                WHERE r.referrer_id = ? AND p.status = 'completed'
            ''', (user_id,))
            completed_referred = cursor.fetchone()[0]

            cursor.execute('''
                SELECT SUM(reward_sela) FROM referrals 
                WHERE referrer_id = ? AND is_claimed = TRUE
            ''', (user_id,))
            claimed_rewards = cursor.fetchone()[0] or 0

            conn.close()

            return {
                'total_referred': total_referred,
                'completed_referred': completed_referred,
                'claimed_rewards': claimed_rewards,
                'pending_rewards': (total_referred - completed_referred) * 5.0
            }

        except Exception as e:
            logger.error(f"❌ Error getting referral stats: {e}")
            return {'total_referred': 0, 'completed_referred': 0, 'claimed_rewards': 0, 'pending_rewards': 0}
