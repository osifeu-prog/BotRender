from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class BuyUI:
    def render(self):
        text = "🛒 **רכישת SELA**\nבחר חבילה:"
        kb = [
            [InlineKeyboardButton("🪙 10 SELA", callback_data="buy_10"),
             InlineKeyboardButton("💎 50 SELA", callback_data="buy_50")],
            [InlineKeyboardButton("🚀 100 SELA", callback_data="buy_100")],
            [InlineKeyboardButton("↩️ חזרה", callback_data="back_to_dashboard")],
        ]
        return text, InlineKeyboardMarkup(kb)
