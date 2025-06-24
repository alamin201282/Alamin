import os
from typing import List

# Bot Token - Get from BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Required channels for verification
REQUIRED_CHANNELS: List[dict] = [
    {
        "name": "Nill Earning Zone",
        "username": "nillearningzone",
        "url": "https://t.me/nillearningzone"
    },
    {
        "name": "Abu Saeid Nill",
        "username": "abusaeidnill1", 
        "url": "https://t.me/abusaeidnill1"
    },
    {
        "name": "Nill TG Teach",
        "username": "nilltgtach",
        "url": "https://t.me/nilltgtach"
    }
]

# Exclusive channel link (only shown after verification)
EXCLUSIVE_CHANNEL = {
    "name": "Join Whatsapp/Telegram OTP Grup",
    "url": "https://t.me/+LW7G5kBBJWNkMDZl"
}

# Bot messages
MESSAGES = {
    "welcome": """
🎯 ═══════════════════════════════
🔥 Join channels to receive access links WhatsApp & Telegram OTP groups - fast and verified! 🚀
═══════════════════════════════ 🎯

🌟 Join These Channels For Exclusive Access:

{}

💥 Ready to unlock premium content? Click 🔍 Verify Membership below!
""",
    
    "verification_start": "🔍 Checking your membership status...",
    
    "not_member": """
❌ You are not a member of: **{}**

Please join this channel first:
{}

After joining, click the 🔍 Check Again button below to verify your status.
""",
    
    "partial_verification": """
📊 PROGRESS: {}/{} Channels Joined ✨

🔥 Remaining Channels to Join:
{}

⚡ Almost there! Join the remaining channels to unlock premium access!
""",
    
    "verification_complete": """
🎊 ═══════════════════════════════
      ✅ VERIFICATION SUCCESS ✅  
═══════════════════════════════ 🎊

🔓 ACCESS GRANTED! 🔓

💎 Your Exclusive Channel Link:
{}

🌟 Welcome to Our Premium Community! 🌟
""",
    
    "verification_error": """
⚠️ Cannot check membership automatically due to channel privacy settings.

**IMPORTANT: Follow these steps to get your exclusive link:**

1. Join ALL required channels using the blue "Join" buttons below
2. After joining all channels, click the GREEN button:
   "✅ I've Joined All Channels - Get Access Now!"
3. You will immediately receive the exclusive channel link

**Already joined all channels?**
Click the GREEN button below to get instant access!
""",
    
    "help": """
🤖 *Bot Commands:*

• /start - Get started with verification process
• /verify - Check your channel membership status
• /help - Show this help message

📝 *How to Get Access:*
1. Use /start to see required channels
2. Join all required channels
3. Click 🔍 Verify Membership
4. Get your exclusive access link!

⚡ Need help? Just use these commands!
"""
}

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
