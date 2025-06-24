import logging
from telegram import Bot
from telegram.error import TelegramError
from typing import List, Tuple, Optional
from config import REQUIRED_CHANNELS

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def check_user_membership(bot: Bot, user_id: int) -> Tuple[List[dict], List[dict]]:
    """
    Check user membership across all required channels.
    
    Args:
        bot: The Telegram bot instance
        user_id: The user ID to check membership for
    
    Returns:
        Tuple[List[dict], List[dict]]: A tuple containing two lists:
            - List of channels the user has joined
            - List of channels the user has not joined
    
    Note:
        If membership cannot be verified due to privacy settings or errors,
        the channel will be added to not_joined_channels for safety.
    """
    joined_channels = []
    not_joined_channels = []
    
    for channel in REQUIRED_CHANNELS:
        channel_username = channel['username']
        try:
            # Try to get chat member status
            member = await bot.get_chat_member(
                chat_id=f"@{channel_username}", 
                user_id=user_id
            )
            
            # Check membership status
            if member.status in ['member', 'administrator', 'creator']:
                joined_channels.append(channel)
                logger.info(
                    "User %s is member of @%s (status: %s)", 
                    user_id, channel_username, member.status
                )
            else:
                not_joined_channels.append(channel)
                logger.info(
                    "User %s is not member of @%s (status: %s)", 
                    user_id, channel_username, member.status
                )
                
        except TelegramError as e:
            error_msg = str(e).lower()
            not_joined_channels.append(channel)
            
            # Log different error cases appropriately
            if "member list is inaccessible" in error_msg:
                logger.warning(
                    "Cannot verify membership for @%s due to privacy settings", 
                    channel_username
                )
            elif "bad request" in error_msg:
                logger.warning(
                    "Bad request while checking @%s: %s", 
                    channel_username, str(e)
                )
            elif "user not found" in error_msg:
                logger.info(
                    "User %s not found in @%s", 
                    user_id, channel_username
                )
            else:
                logger.error(
                    "Error checking membership for @%s: %s", 
                    channel_username, str(e)
                )
    
    return joined_channels, not_joined_channels

def format_channel_list(channels: List[dict], with_links: bool = True) -> str:
    """
    Format a list of channels for display in messages.
    
    Args:
        channels: List of channel dictionaries containing 'name' and 'url'
        with_links: Whether to include HTML links to channels
    
    Returns:
        str: Formatted string with channel list, each on a new line
    """
    if not channels:
        return ""
    
    formatted = []
    for channel in channels:
        if with_links:
            formatted.append(f"🔥 <a href='{channel['url']}'>{channel['name']}</a> ⚡")
        else:
            formatted.append(f"🔥 {channel['name']} ⚡")
    
    return "\n".join(formatted)

def format_remaining_channels(not_joined: List[dict]) -> str:
    """
    Format the list of channels that user still needs to join.
    
    Args:
        not_joined: List of channel dictionaries the user hasn't joined yet
    
    Returns:
        str: Formatted string with remaining channels, each on a new line
    """
    return format_channel_list(not_joined, with_links=True)

async def is_bot_admin_in_channel(bot: Bot, channel_username: str) -> bool:
    """
    Check if the bot has administrator rights in a specific channel.
    
    Args:
        bot: The Telegram bot instance
        channel_username: Username of the channel to check
    
    Returns:
        bool: True if bot is an admin, False otherwise
    """
    try:
        bot_member = await bot.get_chat_member(
            chat_id=f"@{channel_username}", 
            user_id=bot.id
        )
        is_admin = bot_member.status in ['administrator', 'creator']
        
        if is_admin:
            logger.info("Bot has admin rights in @%s", channel_username)
        else:
            logger.warning("Bot lacks admin rights in @%s", channel_username)
            
        return is_admin
        
    except TelegramError as e:
        logger.error(
            "Error checking bot admin status in @%s: %s",
            channel_username, str(e)
        )
        return False

def validate_bot_permissions(bot: Bot) -> List[str]:
    """
    Validate that the bot has all necessary permissions and configuration.
    
    Args:
        bot: The Telegram bot instance to validate
    
    Returns:
        List[str]: List of identified issues, empty if no issues found
    """
    issues = []
    
    # Validate bot token
    if not bot.token or bot.token == "YOUR_BOT_TOKEN_HERE":
        issues.append("Bot token is not properly configured")
        logger.error("Bot token validation failed")
    
    return issues
