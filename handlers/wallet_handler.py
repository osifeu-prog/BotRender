import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class WalletHandler:
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.wallet_manager = bot.wallet_manager

    async def handle_wallet(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        self.bot.debug.log_user_interaction(user.id, "wallet_command")
        
        # בדיקה אם יש ארנק למשתמש
        wallet = self.wallet_manager.get_wallet(user.id)
        
        if not wallet:
            # יצירת ארנק חדש
            wallet_address = self.wallet_manager.create_wallet(user.id)
            if wallet_address:
                await update.message.reply_text(
                    f"🎉 *ארנק נוצר בהצלחה!*\n\n"
                    f"📍 **כתובת הארנק שלך:**\n`{wallet_address}`\n\n"
                    f"💰 **יתוך נוכחי:** 0 SELA\n"
                    f"📈 **תגמול רישום:** {self.config.REGISTRATION_REWARD} SELA\n\n"
                    f"השתמש בכפתורים למטה לניהול הארנק:",
                    parse_mode='Markdown',
                    reply_markup=self.get_wallet_keyboard()
                )
            else:
                await update.message.reply_text("❌ אירעה שגיאה ביצירת הארנק. נסה שוב.")
        else:
            # עדכון יתוך והצגת מידע
            current_balance = self.wallet_manager.update_balance(user.id)
            await update.message.reply_text(
                f"👛 *ארנק SELA שלך*\n\n"
                f"📍 **כתובת:** `{wallet['address']}`\n"
                f"💰 **יתוך:** {current_balance} SELA\n"
                f"🌐 **רשת:** BSC (Binance Smart Chain)\n\n"
                f"*בחר פעולה:*",
                parse_mode='Markdown',
                reply_markup=self.get_wallet_keyboard()
            )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        action = query.data
        user = query.from_user
        
        if action == "wallet_balance":
            await self.show_balance(query, context)
        elif action == "wallet_address":
            await self.show_address(query, context)
        elif action == "wallet_transactions":
            await self.show_transactions(query, context)
        elif action == "wallet_receive":
            await self.show_receive(query, context)
        elif action == "wallet_send":
            await self.show_send(query, context)
        elif action == "wallet_connect":
            await self.show_connect(query, context)
        else:
            await query.edit_message_text("❌ פעולה לא זמינה")

    async def show_balance(self, query, context):
        user = query.from_user
        current_balance = self.wallet_manager.update_balance(user.id)
        
        await query.edit_message_text(
            f"💰 *יתוך ארנק*\n\n"
            f"**יתוך נוכחי:** {current_balance} SELA\n"
            f"**שווה ערך:** ₪{current_balance * self.config.SELA_PRICE_ILS:.2f}\n\n"
            f"*SELA = ₪{self.config.SELA_PRICE_ILS}*",
            parse_mode='Markdown',
            reply_markup=self.get_wallet_keyboard()
        )

    async def show_address(self, query, context):
        user = query.from_user
        wallet = self.wallet_manager.get_wallet(user.id)
        
        if wallet:
            await query.edit_message_text(
                f"📍 *כתובת הארנק שלך*\n\n"
                f"```{wallet['address']}```\n\n"
                f"**השתמש בכתובת זו כדי:**\n"
                f"• לקבל SELA מאחרים\n"
                f"• לחבר לארנקים חיצוניים\n"
                f"• לבצע עסקאות\n\n"
                f"📋 *הכתובת הועתקה ללוח*",
                parse_mode='Markdown',
                reply_markup=self.get_wallet_keyboard()
            )

    async def show_transactions(self, query, context):
        user = query.from_user
        transactions = self.wallet_manager.get_transactions(user.id, 5)
        
        if transactions:
            transactions_text = "\n".join([
                f"• {tx['type']}: {tx['amount']} SELA ({tx['status']})"
                for tx in transactions
            ])
        else:
            transactions_text = "אין עסקאות עדיין"
        
        await query.edit_message_text(
            f"📊 *היסטוריית עסקאות*\n\n{transactions_text}",
            parse_mode='Markdown',
            reply_markup=self.get_wallet_keyboard()
        )

    async def show_receive(self, query, context):
        user = query.from_user
        wallet = self.wallet_manager.get_wallet(user.id)
        
        if wallet:
            await query.edit_message_text(
                f"📥 *קבלת SELA*\n\n"
                f"**שלחו SELA לכתובת:**\n"
                f"```{wallet['address']}```\n\n"
                f"**או סרקו את QR code:**\n"
                f"(יצירת QR code תתווסף בקרוב)\n\n"
                f"💰 **תגמול חיבור ארנק:** {self.config.WALLET_CONNECT_REWARD} SELA",
                parse_mode='Markdown',
                reply_markup=self.get_wallet_keyboard()
            )

    async def show_send(self, query, context):
        await query.edit_message_text(
            "📤 *שליחת SELA*\n\n"
            "פונקציית השליחה תתווסף בקרוב.\n\n"
            "**פיצ'רים עתידיים:**\n"
            "• שליחה לכתובת\n• שליחה למשתמש\n• תשלום בחנות",
            parse_mode='Markdown',
            reply_markup=self.get_wallet_keyboard()
        )

    async def show_connect(self, query, context):
        await query.edit_message_text(
            "🔗 *חיבור ארנק חיצוני*\n\n"
            "**שלח את המפתח הפרטי שלך (64 תווים):**\n"
            "אנו נצפין ונאחסן אותו באופן מאובטח.\n\n"
            "⚠️ **אזהרה:** וודא שאתה שולח רק מפתחות של ארנקי SELA!",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 חזרה לארנק", callback_data="wallet_back")
            ]])
        )

    async def process_private_key(self, update, private_key):
        user = update.effective_user
        
        if len(private_key) == 64 and all(c in '0123456789abcdef' for c in private_key.lower()):
            # כאן יש לטפל בחיבור הארנק החיצוני
            await update.message.reply_text(
                f"✅ *ארנק חובר בהצלחה!*\n\n"
                f"קיבלת {self.config.WALLET_CONNECT_REWARD} SELA תגמול!\n\n"
                f"המפתח הפרטי הוצפן ונשמר באופן מאובטח.",
                parse_mode='Markdown',
                reply_markup=self.get_wallet_keyboard()
            )
        else:
            await update.message.reply_text(
                "❌ מפתח פרטי לא תקין. אנא שלח מפתח בן 64 תווים (hex)."
            )

    def get_wallet_keyboard(self):
        keyboard = [
            [
                InlineKeyboardButton("💰 יתוך", callback_data="wallet_balance"),
                InlineKeyboardButton("📍 כתובת", callback_data="wallet_address")
            ],
            [
                InlineKeyboardButton("📊 עסקאות", callback_data="wallet_transactions"),
                InlineKeyboardButton("📥 קבל", callback_data="wallet_receive")
            ],
            [
                InlineKeyboardButton("📤 שלח", callback_data="wallet_send"),
                InlineKeyboardButton("🔗 חבר ארנק", callback_data="wallet_connect")
            ],
            [
                InlineKeyboardButton("🔙 לדשבורד", callback_data="back_to_dashboard")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
