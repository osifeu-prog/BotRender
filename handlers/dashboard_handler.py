from ui.dashboard_ui import DashboardUI

class DashboardHandler:
    def __init__(self, bot):
        self.bot = bot
        self.ui = DashboardUI()

    async def handle_dashboard(self, update, context):
        await self.show_dashboard(update, context)

    async def show_dashboard(self, update, context):
        text, kb = self.ui.render()
        if update.message:
            await update.message.reply_text(text, reply_markup=kb, parse_mode='Markdown')
        else:
            await update.callback_query.edit_message_text(text, reply_markup=kb, parse_mode='Markdown')

    async def handle_callback(self, update, context):
        await update.callback_query.edit_message_text("🏗️ דשבורד – פעולה בדרך")
