import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ui.nft_ui import NFTUI

logger = logging.getLogger(__name__)

class NFTHandler:
    def __init__(self, bot):
        self.bot = bot
        self.ui = NFTUI()

    async def handle_nft(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        self.bot.debug.log_user_interaction(user.id, "nft_command")

        user_nfts = self.bot.nft_manager.get_user_nfts(user.id)
        nft_text, reply_markup = self.ui.create_nft_gallery(user_nfts)

        await update.message.reply_text(nft_text, reply_markup=reply_markup, parse_mode='Markdown')

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        user = query.from_user
        action = query.data

        try:
            if action == "nft_main":
                await self.show_nft_gallery(user, query)
            elif action == "nft_show":
                await self.show_my_nfts(user, query)
            elif action == "nft_share":
                await self.share_nft(user, query)
            elif action == "nft_community":
                await self.show_community_nfts(user, query)
            elif action == "nft_upload":
                await self.request_nft_upload(user, query)
            elif action == "nft_create":
                await self.create_custom_nft(user, query)
            elif action == "nft_competitions":
                await self.show_nft_competitions(user, query)
            else:
                await query.edit_message_text(f"🛠️ NFT action not implemented: {action}")

        except Exception as e:
            logger.error(f"Error in NFT callback: {e}")
            await query.edit_message_text("❌ אירעה שגיאה. נא לנסות שוב.")

    async def show_nft_gallery(self, user, query):
        user_nfts = self.bot.nft_manager.get_user_nfts(user.id)
        nft_text, reply_markup = self.ui.create_nft_gallery(user_nfts)
        await query.edit_message_text(nft_text, reply_markup=reply_markup, parse_mode='Markdown')

    async def show_my_nfts(self, user, query):
        user_nfts = self.bot.nft_manager.get_user_nfts(user.id)

        if user_nfts:
            nft_text = "🎨 **האוסף האישי שלך**\n\n"

            for i, nft in enumerate(user_nfts, 1):
                stars = "⭐" * nft.get('rarity', 1)
                nft_text += f"""**{i}. {nft['name']}** {stars}
🆔 `{nft['token_id']}`
📅 {str(nft.get('created_at'))[:10]}
📝 {nft.get('description','')}

"""

            nft_text += f"📊 **סה\"כ:** {len(user_nfts)} NFTs באוסף"
        else:
            nft_text = """
🚀 **עדיין אין לך NFTs!**

🎁 **כיצד לקבל NFTs:**
• 🛒 **רכישת SELA** - כל רכישה מזכה ב-NFT
• 🏆 **משימות** - השלם משימות וקבל NFTs
• 🎯 **תחרויות** - השתתף וזכה ב-NFTs נדירים
• 💎 **קהילה** - תרומה לקהילה מזכה ב-NFTs

💫 **התחל לבנות את האוסף שלך היום!**
"""

        keyboard = [
            [InlineKeyboardButton("📱 שתף אוסף", callback_data="nft_share")],
            [InlineKeyboardButton("🔼 העלה NFT", callback_data="nft_upload")],
            [InlineKeyboardButton("↩️ חזרה לגלריה", callback_data="nft_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(nft_text, reply_markup=reply_markup, parse_mode='Markdown')

    async def share_nft(self, user, query):
        user_nfts = self.bot.nft_manager.get_user_nfts(user.id)

        if user_nfts:
            share_text = f"""
📱 **שתף את אוסף ה-NFT שלך!**

🏆 **אוסף SELA אישי**
👤 **בעלים:** {user.first_name}
🎨 **NFTs:** {len(user_nfts)}
⭐ **NFT מוביל:** {user_nfts[0]['name']}

💎 **הצטרף למהפכת SELA!**
🎯 קנה SELA וקבל NFT בלעדי
🚀 www.sela-community.com

#SELA #NFT #Crypto #{user.first_name}
"""
        else:
            share_text = """
📱 **שתף את אהבתך ל-NFTs!**

🎨 **אספן NFT לעתיד**
👤 **חבר קהילת SELA**

💎 **הצטרף למהפכת SELA!**
🎯 קנה SELA וקבל NFT בלעדי
🚀 התחל לבנות אוסף דיגיטלי

#SELA #NFT #Crypto #FutureCollector
"""

        keyboard = [
            [InlineKeyboardButton("🎯 הצטרף עכשיו", url="https://t.me/your_bot_name")],
            [InlineKeyboardButton("↩️ חזרה", callback_data="nft_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(share_text, reply_markup=reply_markup, parse_mode='Markdown')

    async def show_community_nfts(self, user, query):
        community_text = """
╔══════════════════════════════╗
║     🎨 אוסף הקהילה           ║
╚══════════════════════════════╝

👥 **סטטיסטיקות אוסף:**

• 🎨 **NFTs בקהילה:** 2,847
• 💎 **אספנים:** 1,247
• 🏆 **אספנים מובילים:** 23
• ⭐ **NFTs ממוצע לאספן:** 2.3

🚀 **האוסף הפופולרי:**

🥇 **SELA Founder #001**
• בעלים: @CryptoKing
• ערך משוער: 10,000 ₪
• נדירות: ⭐⭐⭐⭐⭐

🥈 **SELA Elite #042**  
• בעלים: @NFTQueen
• ערך משוער: 5,000 ₪
• נדירות: ⭐⭐⭐⭐

🥉 **SELA Starter #789**
• בעלים: @BlockchainPro
• ערך משוער: 2,500 ₪
• נדירות: ⭐⭐⭐

🎯 **אספנים מובילים:**
1. @CryptoKing - 47 NFTs
2. @NFTQueen - 32 NFTs  
3. @BlockchainPro - 28 NFTs
4. @SELALover - 25 NFTs
5. @DigitalArt - 23 NFTs

💫 **הצטרף למועדון האספנים!**
"""
        await query.edit_message_text(community_text, parse_mode='Markdown')

    async def request_nft_upload(self, user, query):
        upload_text = """
╔══════════════════════════════╗
║     🔼 העלאת NFT             ║
╚══════════════════════════════╝

🎨 **העלה תמונה ל-NFT אישי!**

📝 **דרישות:**
• פורמטים: JPG, PNG, GIF
• גודל מקסימלי: 10MB
• רזולוציה מומלצת: 1000x1000px
• תוכן: מקורי וייחודי

⚡ **תהליך ההעלאה:**
1. שלח את התמונה כ-**קובץ** (לא כתמונה)
2. הוסף שם ל-NFT
3. כתוב תיאור
4. הגדר נדירות (1-5 כוכבים)

🎁 **יתרונות:**
• NFT אישי וייחודי
• שיתוף בקהילה
• ערך אספני
• גישה לקבוצת אספנים

⚠️ **תנאים:**
• זכויות יוצרים בלעדיות
• תוכן הולם
• איכות תמונה טובה

📤 **שלח עכשיו את התמונה שלך!**
"""
        await query.edit_message_text(upload_text, parse_mode='Markdown')

    async def create_custom_nft(self, user, query):
        create_text = """
╔══════════════════════════════╗
║     🎨 יצירת NFT             ║
╚══════════════════════════════╝

✨ **צור NFT אישי ומקורי!**

🛠️ **אפשרויות יצירה:**

🎯 **NFT בסיסי** - 10 SELA
• תמונה אחת
• שם ותיאור
• נדירות: ⭐⭐

💎 **NFT מתקדם** - 25 SELA  
• עד 3 תמונות
• אנימציה בסיסית
• נדירות: ⭐⭐⭐
• תכונות מיוחדות

🚀 **NFT פרימיום** - 50 SELA
• גלריית תמונות
• אנימציה מתקדמת
• נדירות: ⭐⭐⭐⭐
• תכונות בלעדיות
• חשיפה בקהילה

👑 **NFT אגדי** - 100 SELA
• עיצוב מותאם אישית
• אנימציה מורכבת
• נדירות: ⭐⭐⭐⭐⭐
• תואר אספן
• קבוצת מייסדים

📝 **תהליך היצירה:**
1. בחר חבילה
2. העלה תוכן
3. הגדר מאפיינים
4. אשר ותשלם
5. קבל את ה-NFT שלך

🎯 **בחר חבילה:**
"""

        keyboard = [
            [
                InlineKeyboardButton("🎯 בסיסי - 10 SELA", callback_data="nft_create_basic"),
                InlineKeyboardButton("💎 מתקדם - 25 SELA", callback_data="nft_create_advanced")
            ],
            [
                InlineKeyboardButton("🚀 פרימיום - 50 SELA", callback_data="nft_create_premium"),
                InlineKeyboardButton("👑 אגדי - 100 SELA", callback_data="nft_create_legendary")
            ],
            [InlineKeyboardButton("↩️ חזרה", callback_data="nft_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(create_text, reply_markup=reply_markup, parse_mode='Markdown')

    async def show_nft_competitions(self, user, query):
        competitions_text = """
╔══════════════════════════════╗
║     🏆 תחרויות NFT           ║
╚══════════════════════════════╝

🎯 **תחרויות פעילות:**

🥇 **אספן החודש** 
• **פרס:** 100 SELA + NFT בלעדי
• **תיאור:** האספן עם הכי הרבה NFTs חדשים
• **תאריך:** עד סוף החודש
• **משתתפים:** 247

🎨 **עיצוב NFT**
• **פרס:** NFT אגדי מותאם אישית
• **תיאור:** עיצוב ה-NFT היצירתי ביותר
• **תאריך:** 7 ימים נוספים
• **משתתפים:** 89

📱 **Influencer השבוע**
• **פרס:** 50 SELA + חשיפה
• **תיאור:** השיתוף היצירתי ביותר
• **תאריך:** 3 ימים נוספים
• **משתתפים:** 156

💎 **מייסד החודש**
• **פרס:** 200 SELA + תואר מייסד
• **תיאור:** התרומה המשמעותית ביותר לקהילה
• **תאריך:** 14 ימים נוספים
• **משתתפים:** 45

📅 **לוח זמנים:**
• 🗓️ **הגשה:** עד תאריך היעד
• 📢 **הכרזה:** 3 ימים לאחר מכן
• 🎁 **חלוקת פרסים:** 24 שעות מההכרזה

🚀 **הצטרף ותחרות!**
"""

        keyboard = [
            [InlineKeyboardButton("🎯 השתתף עכשיו", callback_data="nft_join_competition")],
            [InlineKeyboardButton("📊 לוח תוצאות", callback_data="nft_leaderboard")],
            [InlineKeyboardButton("↩️ חזרה", callback_data="nft_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(competitions_text, reply_markup=reply_markup, parse_mode='Markdown')

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        photo = update.message.photo[-1]

        self.bot.debug.log_user_interaction(user.id, "nft_photo_upload")

        context.user_data['pending_nft'] = {
            'photo': photo,
            'step': 'waiting_for_name'
        }

        await update.message.reply_text(
            "📸 **תמונה התקבלה!**\n\n"
            "🎨 כעת שלח את הפרטים הבאים:\n"
            "• **שם ה-NFT**\n"  
            "• **תיאור**\n"
            "• **רמת נדירות** (1-5 כוכבים)\n\n"
            "✍️ **שלח את הפרטים בפורמט:**\n"
            "`שם; תיאור; 3`\n\n"
            "📝 **דוגמה:**\n"
            "`הציור שלי; זה תיאור של ה-NFT שלי; 3`"
        )

    async def handle_nft_details(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        message_text = update.message.text

        if 'pending_nft' not in context.user_data:
            await update.message.reply_text("❌ לא נמצאה תמונה ממתינה. אנא התחל בהעלאת תמונה.")
            return

        try:
            parts = message_text.split(';')
            if len(parts) != 3:
                await update.message.reply_text(
                    "❌ פורמט לא תקין. אנא השתמש בפורמט:\n"
                    "`שם; תיאור; מספר_נדירות`"
                )
                return

            name = parts[0].strip()
            description = parts[1].strip()

            try:
                rarity = int(parts[2].strip())
                if rarity < 1 or rarity > 5:
                    raise ValueError
            except ValueError:
                await update.message.reply_text("❌ נדירות חייבת להיות מספר בין 1 ל-5")
                return

            nft_result = self.bot.nft_manager.create_custom_nft(
                user.id, name, description, None, rarity
            )

            if nft_result['success']:
                await update.message.reply_text(
                    f"🎉 **NFT נוצר בהצלחה!**\n\n"
                    f"**שם:** {name}\n"
                    f"**תיאור:** {description}\n"
                    f"**נדירות:** {'⭐' * rarity}\n"
                    f"**מזהה:** `{nft_result['token_id']}`\n\n"
                    f"💫 ה-NFT נוסף לאוסף שלך!"
                )

                del context.user_data['pending_nft']
            else:
                await update.message.reply_text(
                    f"❌ **שגיאה ביצירת NFT:** {nft_result.get('error', 'שגיאה לא ידועה')}"
                )

        except Exception as e:
            logger.error(f"Error processing NFT details: {e}")
            await update.message.reply_text("❌ אירעה שגיאה בעיבוד הפרטים. אנא נסה שוב.")
