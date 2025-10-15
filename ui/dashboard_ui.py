from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class DashboardUI:
    def render(self, user_data=None):
        keyboard = [
            [
                InlineKeyboardButton("💰 ארנק", callback_data="dashboard_wallet"),
                InlineKeyboardButton("🛒 קניה", callback_data="dashboard_buy")
            ],
            [
                InlineKeyboardButton("🎨 NFT", callback_data="dashboard_nft"),
                InlineKeyboardButton("🏠 בית", callback_data="back_to_dashboard")
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = "🏠 **דשבורד SELA**\nבחר אפשרות:"
        return text, reply_markup
