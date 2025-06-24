import logging
from typing import List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from config import MESSAGES, REQUIRED_CHANNELS, EXCLUSIVE_CHANNEL
from utils import check_user_membership, format_channel_list, format_remaining_channels

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    
    # Format the required channels list
    channels_text = format_channel_list(REQUIRED_CHANNELS)
    welcome_message = MESSAGES["welcome"].format(channels_text)
    
    # Create inline keyboard with verify button
    keyboard = [[InlineKeyboardButton("🔍 Verify Membership", callback_data="verify")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    await update.message.reply_text(
        MESSAGES["help"],
        parse_mode=ParseMode.HTML
    )

async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /verify command."""
    await verify_membership(update, context)

async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the verify button callback."""
    query = update.callback_query
    await query.answer()
    
    # Edit the message to show verification in progress
    await query.edit_message_text(
        text=MESSAGES["verification_start"],
        parse_mode=ParseMode.HTML
    )
    
    # Perform verification
    await verify_membership(update, context, is_callback=True)

async def force_verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the force verify button callback for users who claim to have joined all channels."""
    query = update.callback_query
    await query.answer("🎉 SUCCESS! Here's your exclusive channel link!")
    
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) manually verified - granting access to exclusive channel")
    
    # Show verification complete message directly
    message = MESSAGES["verification_complete"].format(
        f"[{EXCLUSIVE_CHANNEL['name']}]({EXCLUSIVE_CHANNEL['url']})"
    )
    
    # Create keyboard with join button for exclusive channel
    keyboard = [[InlineKeyboardButton("🚀 Join Now Whatsapp/Telegram OTP Grup", url=EXCLUSIVE_CHANNEL['url'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=message,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

async def verify_membership(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool = False) -> None:
    """Verify user membership across all required channels."""
    user = update.effective_user
    logger.info(f"Verifying membership for user {user.id} ({user.username})")
    
    try:
        # Check membership status
        joined_channels, not_joined_channels = await check_user_membership(
            context.bot, user.id
        )
        
        # Determine response based on verification results
        if not not_joined_channels:  # All channels joined
            await handle_verification_complete(update, context, is_callback)
        elif not joined_channels:  # No channels joined
            await handle_no_membership(update, context, not_joined_channels[0], is_callback)
        else:  # Partial membership
            await handle_partial_membership(update, context, joined_channels, not_joined_channels, is_callback)
            
    except Exception as e:
        logger.error(f"Error during verification for user {user.id}: {str(e)}")
        await handle_verification_error(update, context, is_callback)

async def handle_verification_complete(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool = False) -> None:
    """Handle successful verification."""
    message = MESSAGES["verification_complete"].format(
        f"[{EXCLUSIVE_CHANNEL['name']}]({EXCLUSIVE_CHANNEL['url']})"
    )
    
    keyboard = [[InlineKeyboardButton("🚀 Join Now Whatsapp/Telegram OTP Grup", url=EXCLUSIVE_CHANNEL['url'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if is_callback:
        await update.callback_query.edit_message_text(
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

async def handle_no_membership(update: Update, context: ContextTypes.DEFAULT_TYPE, channel: dict, is_callback: bool = False) -> None:
    """Handle case where user hasn't joined any channel."""
    message = MESSAGES["not_member"].format(
        channel['name'],
        channel['url']
    )
    
    keyboard = [
        [InlineKeyboardButton(f"Join {channel['name']}", url=channel['url'])],
        [InlineKeyboardButton("🔍 Check Again", callback_data="verify")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if is_callback:
        await update.callback_query.edit_message_text(
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

async def handle_partial_membership(update: Update, context: ContextTypes.DEFAULT_TYPE, joined: List[dict], not_joined: List[dict], is_callback: bool = False) -> None:
    """Handle case where user has joined some but not all channels."""
    remaining_channels = format_remaining_channels(not_joined)
    message = MESSAGES["partial_verification"].format(
        len(joined),
        len(REQUIRED_CHANNELS),
        remaining_channels
    )
    
    keyboard = [
        [InlineKeyboardButton(f"Join {channel['name']}", url=channel['url'])] for channel in not_joined
    ]
    keyboard.append([InlineKeyboardButton("🔍 Check Again", callback_data="verify")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if is_callback:
        await update.callback_query.edit_message_text(
            text=message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            text=message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

async def handle_verification_error(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool = False) -> None:
    """Handle verification errors."""
    message = MESSAGES["verification_error"]
    
    keyboard = [
        [InlineKeyboardButton(f"Join {channel['name']}", url=channel['url'])] for channel in REQUIRED_CHANNELS
    ]
    keyboard.append([InlineKeyboardButton("✅ I've Joined All Channels - Get Access Now!", callback_data="force_verify")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if is_callback:
        await update.callback_query.edit_message_text(
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

async def handle_verification_complete(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool) -> None:
    """Handle successful verification of all channels."""
    user = update.effective_user
    logger.info(f"User {user.id} successfully verified all channels")
    
    message = MESSAGES["verification_complete"].format(
        f"[{EXCLUSIVE_CHANNEL['name']}]({EXCLUSIVE_CHANNEL['url']})"
    )
    
    # Create keyboard with join button for exclusive channel
    keyboard = [[InlineKeyboardButton("🚀 Join Now Whatsapp/Telegram OTP Grup", url=EXCLUSIVE_CHANNEL['url'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if is_callback:
        await update.callback_query.edit_message_text(
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

async def handle_no_membership(update: Update, context: ContextTypes.DEFAULT_TYPE, first_channel: dict, is_callback: bool) -> None:
    """Handle case where user hasn't joined any channels."""
    # Show all channels that need to be joined
    channels_text = format_channel_list(REQUIRED_CHANNELS)
    message = f"""🚫 ACCESS DENIED 🚫

🔥 Join All Channels First:

{channels_text}

⚡ Then click 'Verify Again' for premium access!"""
    
    # Create keyboard with join buttons for all channels and verify button
    keyboard = []
    for channel in REQUIRED_CHANNELS:
        keyboard.append([InlineKeyboardButton(f"📱 Join {channel['name']}", url=channel['url'])])
    keyboard.append([InlineKeyboardButton("🔍 Verify Again", callback_data="verify")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if is_callback:
        await update.callback_query.edit_message_text(
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

async def handle_partial_membership(update: Update, context: ContextTypes.DEFAULT_TYPE, joined: list, not_joined: list, is_callback: bool) -> None:
    """Handle case where user has joined some but not all channels."""
    remaining_channels = format_remaining_channels(not_joined)
    message = MESSAGES["partial_verification"].format(
        len(joined),
        len(REQUIRED_CHANNELS),
        remaining_channels
    )
    
    # Create keyboard with join buttons for remaining channels and verify button
    keyboard = []
    for channel in not_joined:
        keyboard.append([InlineKeyboardButton(f"📱 Join {channel['name']}", url=channel['url'])])
    keyboard.append([InlineKeyboardButton("🔍 Verify Again", callback_data="verify")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if is_callback:
        await update.callback_query.edit_message_text(
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

async def handle_verification_error(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool) -> None:
    """Handle verification errors."""
    # Create keyboard with join buttons for all channels and special access button
    keyboard = []
    for channel in REQUIRED_CHANNELS:
        keyboard.append([InlineKeyboardButton(f"📱 Join {channel['name']}", url=channel['url'])])
    
    # Add special access button for users who have joined all channels
    keyboard.append([InlineKeyboardButton("✅ I've Joined All Channels - Get Access Now!", callback_data="force_verify")])
    keyboard.append([InlineKeyboardButton("🔄 Try Auto-Verify Again", callback_data="verify")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if is_callback:
        await update.callback_query.edit_message_text(
            text=MESSAGES["verification_error"],
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            MESSAGES["verification_error"],
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    await update.message.reply_text(
        "❓ Unknown command. Use /help to see available commands.",
        parse_mode=ParseMode.HTML
    )

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by Updates."""
    logger.error(f"Exception while handling an update: {context.error}")
    
    # If it's an update with a message, try to inform the user
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "⚠️ An error occurred. Please try again later."
            )
        except Exception as e:
            logger.error(f"Failed to send error message to user: {e}")
