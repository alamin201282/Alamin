import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN, LOG_LEVEL
from handlers import (
    start_command, help_command, verify_command, verify_callback, force_verify_callback,
    unknown_command, error_handler
)
from utils import validate_bot_permissions

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL.upper())
)
logger = logging.getLogger(__name__)

class TelegramVerificationBot:
    """Main bot class for handling Telegram verification bot."""
    
    def __init__(self, token: str):
        """Initialize the bot with the given token."""
        self.token = token
        self.application = None
    
    def setup_handlers(self) -> None:
        """Set up all command and callback handlers."""
        app = self.application
        
        # Command handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("verify", verify_command))
        
        # Callback query handlers
        app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))
        app.add_handler(CallbackQueryHandler(force_verify_callback, pattern="force_verify"))
        
        # Unknown command handler (should be last)
        app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
        
        # Error handler
        app.add_error_handler(error_handler)
        
        logger.info("All handlers have been set up successfully")
    
    async def post_init(self, application: Application) -> None:
        """Post initialization hook."""
        bot = application.bot
        bot_info = await bot.get_me()
        logger.info(f"Bot initialized: @{bot_info.username} ({bot_info.first_name})")
        
        # Validate bot permissions
        issues = validate_bot_permissions(bot)
        if issues:
            logger.warning(f"Bot configuration issues: {', '.join(issues)}")
    
    def run(self) -> None:
        """Run the bot."""
        if not self.token or self.token == "YOUR_BOT_TOKEN_HERE":
            logger.error("Bot token is not configured. Please set BOT_TOKEN environment variable.")
            return
        
        try:
            # Create application
            self.application = Application.builder().token(self.token).post_init(self.post_init).build()
            
            # Setup handlers
            self.setup_handlers()
            
            logger.info("Starting bot...")
            
            # Start the bot
            self.application.run_polling(
                allowed_updates=["message", "callback_query"],
                drop_pending_updates=True
            )
            
        except Exception as e:
            logger.error(f"Failed to start bot: {str(e)}")
            raise
    
    def stop(self) -> None:
        """Stop the bot gracefully."""
        if self.application:
            logger.info("Stopping bot...")
            self.application.stop()

def create_bot() -> TelegramVerificationBot:
    """Factory function to create a bot instance."""
    return TelegramVerificationBot(BOT_TOKEN)

if __name__ == "__main__":
    bot = create_bot()
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {str(e)}")
    finally:
        if hasattr(bot, 'application') and bot.application:
            bot.stop()
