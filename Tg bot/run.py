#!/usr/bin/env python3
"""
Telegram Channel Verification Bot

This bot verifies user membership in multiple Telegram channels
before granting access to exclusive content.

Usage:
    python run.py

Environment Variables:
    BOT_TOKEN - Your Telegram bot token from BotFather
    LOG_LEVEL - Logging level (DEBUG, INFO, WARNING, ERROR)
"""

import sys
import os
import asyncio
import logging
from bot import create_bot

def main():
    """Main entry point for the bot."""
    print("🤖 Telegram Channel Verification Bot")
    print("=" * 40)
    
    # Configure logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    
    # Check if bot token is provided
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token or bot_token == "YOUR_BOT_TOKEN_HERE":
        error_msg = "\n".join([
            "❌ Error: BOT_TOKEN environment variable is not set!",
            "\nTo fix this:",
            "1. Get a bot token from @BotFather on Telegram",
            "2. Set the environment variable:",
            "   On Windows: set BOT_TOKEN=your_token_here",
            "   On Linux/Mac: export BOT_TOKEN=your_token_here",
            "3. Or create a .env file with: BOT_TOKEN=your_token_here"
        ])
        print(error_msg)
        logger.error("Bot token not configured")
        return 1
    
    try:
        # Create and run the bot
        bot = create_bot()
        logger.info("Bot created successfully")
        
        print("🚀 Starting bot...")
        print("Press Ctrl+C to stop")
        print("-" * 40)
        
        bot.run()
        
    except KeyboardInterrupt:
        print("\n⏹️  Bot stopped by user")
        logger.info("Bot stopped by user")
        return 0
    except Exception as e:
        error_msg = f"\n💥 Bot crashed: {str(e)}"
        print(error_msg)
        logger.exception("Bot crashed with exception:")
        return 1
    finally:
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    sys.exit(main())
