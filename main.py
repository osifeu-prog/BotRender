import logging
import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import Config
from utils.debug_config import DebugConfig

# imports למנהלים
from managers.wallet_manager import WalletManager
from managers.nft_manager import NFTManager
from managers.distribution_manager import DistributionManager
from managers.reward_manager import RewardManager

# imports ל-handlers
from handlers.start_handler import StartHandler
from handlers.wallet_handler import WalletHandler
from handlers.nft_handler import NFTHandler
from handlers.buy_handler import BuyHandler
from handlers.dashboard_handler import DashboardHandler

logger = logging.getLogger(__name__)

class SelaBot:
    def __init__(self):
        self.debug = DebugConfig()
        self.config = Config()
        self.debug.log_bot_start()

        # אתחול מנהלים - תיקון קריטי!
        self.wallet_manager = WalletManager(self.config)
        self.nft_manager = NFTManager()
        self.distribution_manager = DistributionManager(self)  # שים לב - מעביר את self
        self.reward_manager = RewardManager(self)  # שים לב - מעביר את self

        # אתחול handlers
        self.start_handler = StartHandler(self)
        self.wallet_handler = WalletHandler(self)
        self.nft_handler = NFTHandler(self)
        self.buy_handler = BuyHandler(self)
        self.dashboard_handler = DashboardHandler(self)

        if not self.config.BOT_TOKEN:
            logger.error("❌ BOT_TOKEN not found!")
            return

        try:
            self.application = Application.builder().token(self.config.BOT_TOKEN).build()
            self.setup_handlers()
            logger.info("✅ SELA Bot initialized successfully!")
        except Exception as e:
            self.debug.log_error("Bot Initialization", e)
            raise

    def setup_handlers(self):
        # handlers בסיסיים
        self.application.add_handler(CommandHandler("start", self.start_handler.handle_start))
        self.application.add_handler(CommandHandler("help", self.start_handler.handle_help))

        # handlers לפי נושאים
        self.application.add_handler(CommandHandler("wallet", self.wallet_handler.handle_wallet))
        self.application.add_handler(CommandHandler("nft", self.nft_handler.handle_nft))
        self.application.add_handler(CommandHandler("buy", self.buy_handler.handle_buy))
        self.application.add_handler(CommandHandler("dashboard", self.dashboard_handler.handle_dashboard))

        # callback handlers
        self.application.add_handler(CallbackQueryHandler(self.handle_callback, pattern=".*"))

        # message handler
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        # photo handler for NFT uploads
        self.application.add_handler(MessageHandler(filters.PHOTO, self.nft_handler.handle_photo))

        # error handler
        self.application.add_error_handler(self.error_handler)

    async def handle_callback(self, update, context):
        query = update.callback_query
        await query.answer()

        action = query.data
        user = query.from_user

        self.debug.log_user_interaction(user.id, f"callback_{action}")

        # ניתוב לפי סוג הפעולה
        if action.startswith("wallet_"):
            await self.wallet_handler.handle_callback(update, context)
        elif action.startswith("nft_"):
            await self.nft_handler.handle_callback(update, context)
        elif action.startswith("buy_"):
            await self.buy_handler.handle_callback(update, context)
        elif action.startswith("dashboard_"):
            await self.dashboard_handler.handle_callback(update, context)
        elif action == "back_to_dashboard":
            await self.dashboard_handler.show_dashboard(update, context)
        else:
            await query.edit_message_text(f"🛠️ Action not implemented: {action}")

    async def handle_message(self, update, context):
        user = update.effective_user
        message_text = update.message.text

        self.debug.log_user_interaction(user.id, f"message: {message_text[:50]}")

        # טיפול בהודעות טקסט לפי הקשר
        if len(message_text) == 64 and all(c in '0123456789abcdef' for c in message_text.lower()):
            await self.wallet_handler.process_private_key(update, message_text)
        elif context.user_data.get('pending_nft'):
            await self.nft_handler.handle_nft_details(update, context)
        else:
            await self.start_handler.show_main_menu(update)

    async def error_handler(self, update, context):
        logger.error(f"Exception while handling an update: {context.error}")

        from telegram.error import BadRequest
        if isinstance(context.error, BadRequest) and "Can't parse entities" in str(context.error):
            logger.error("Markdown parsing error")
            try:
                if update and update.callback_query:
                    await update.callback_query.message.reply_text(
                        "❌ אירעה שגיאה בתצוגה. נא לנסות שוב."
                    )
            except:
                pass
        else:
            # שגיאות כלליות
            try:
                if update and update.effective_user:
                    error_message = "❌ אירעה שגיאה בלתי צפויה. אנא נסה שוב או פנה לתמיכה."
                    if update.callback_query:
                        await update.callback_query.message.reply_text(error_message)
                    elif update.message:
                        await update.message.reply_text(error_message)
            except Exception as e:
                logger.error(f"Error while sending error message: {e}")

    def run(self):
        try:
            logger.info("🚀 Starting SELA Bot...")
            self.application.run_polling()
        except Exception as e:
            self.debug.log_error("Bot Runtime", e)
            logger.error(f"Bot crashed: {e}")
            raise

def main():
    bot = SelaBot()
    bot.run()

if __name__ == '__main__':
    main()
