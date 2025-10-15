from ui.wallet_ui import WalletUI

class WalletHandler:
    def __init__(self, bot):
        self.bot = bot
        self.ui = WalletUI()

    async def handle_wallet(self, update, context):
        w = self.bot.wallet_manager.get_wallet(update.effective_user.id)
        text, kb = self.ui.create_wallet_interface(w)
        await update.message.reply_text(text, reply_markup=kb, parse_mode='Markdown')

    async def handle_callback(self, update, context):
        q = update.callback_query
        if q.data == "wallet_create":
            res = self.bot.wallet_manager.create_wallet(q.from_user.id)
            if res.get("success"):
                w = self.bot.wallet_manager.get_wallet(q.from_user.id)
                text, kb = self.ui.create_wallet_interface(w)
                await q.edit_message_text(text, reply_markup=kb, parse_mode='Markdown')
            else:
                await q.edit_message_text("❌ שגיאה ביצירת ארנק")
        else:
            await q.edit_message_text("🛠️ פעולה בארנק בפיתוח")

    async def process_private_key(self, update, key):
        await update.message.reply_text("🔐 מפתח פרטי התקבל (דמו)")
