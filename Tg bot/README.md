# Telegram Channel Verification Bot 🤖

A Telegram bot that manages channel membership verification and provides access to exclusive content after users join required channels.

## Features ✨

- Automatic channel membership verification
- Support for multiple required channels
- Interactive buttons and user-friendly messages
- Fallback mechanism for channels with privacy restrictions
- Comprehensive error handling and logging

## Prerequisites 📋

- Python 3.7 or higher
- python-telegram-bot library
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)

## Installation 🚀

1. Clone this repository:
```bash
git clone <repository-url>
cd telegram-verification-bot
```

2. Install dependencies:
```bash
pip install python-telegram-bot
```

3. Configure the bot:
   - Get a bot token from [@BotFather](https://t.me/BotFather)
   - Set the environment variable:
     ```bash
     # On Windows
     set BOT_TOKEN=your_token_here
     
     # On Linux/Mac
     export BOT_TOKEN=your_token_here
     ```
   - Or create a `.env` file with:
     ```
     BOT_TOKEN=your_token_here
     ```

## Configuration ⚙️

Edit `config.py` to customize:
- Required channels list
- Exclusive channel information
- Bot messages and prompts

## Usage 📱

1. Start the bot:
```bash
python run.py
```

2. Available commands:
- `/start` - Get started with verification process
- `/verify` - Check channel membership status
- `/help` - Show help message

## Bot Flow 🔄

1. User starts the bot
2. Bot displays required channels
3. User joins the channels
4. User verifies membership
5. Upon successful verification, user gets access to exclusive content

## Error Handling 🛠️

- Handles channel privacy restrictions
- Provides fallback verification method
- Comprehensive logging for debugging

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.
   