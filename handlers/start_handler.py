class StartHandler:
    def __init__(self, bot):
        self.bot = bot

    async def handle_start(self, update, context):
        await self.show_main_menu(update)

    async def handle_help(self, update, context):
        await update.message.reply_text("❓ עזרה: /start /wallet /nft /buy /dashboard")

    async def show_main_menu(self, update):
        await update.message.reply_text("🏠 ברוך הבא ל-SELA! השתמש בתפריט או בפקודות.")
