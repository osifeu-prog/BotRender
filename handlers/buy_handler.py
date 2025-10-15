from ui.buy_ui import BuyUI

class BuyHandler:
    def __init__(self, bot):
        self.bot = bot
        self.ui = BuyUI()

    async def handle_buy(self, update, context):
        text, kb = self.ui.render()
        await update.message.reply_text(text, reply_markup=kb, parse_mode='Markdown')

    async def handle_callback(self, update, context):
        q = update.callback_query
        data = q.data
        amounts = {"buy_10":10, "buy_50":50, "buy_100":100}
        amt = amounts.get(data)
        if amt:
            info = self.bot.distribution_manager.create_purchase_order(q.from_user.id, amt)
            bonuses = "\n".join(f"• {b}" for b in info['bonuses'])
            msg = f"💳 הזמנת רכישה #{info['purchase_id']}\n🪙 {info['sela_amount']} SELA\n💸 {info['total_price_ils']:,.0f} ₪\n🎁 {info['nft_name']}\n\n{bonuses}\n\n{info['payment_instructions']}"
            await q.edit_message_text(msg, parse_mode='Markdown')
        else:
            await q.edit_message_text("🛠️ קניה מותאמת בקרוב")
