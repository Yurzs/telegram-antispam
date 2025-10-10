# telegram-antispam

Telegram bot for filtering channel comments and preventing spam in discussion groups.

## Features

- 🛡️ **Automatic spam filtering**: Detects and removes messages with external links
- ✅ **Channel integration**: Automatically allows links to the connected channel
- 👮 **Admin-friendly**: Admins can post any links without restrictions
- ⚙️ **Easy configuration**: Simple commands to manage the bot
- 🐳 **Docker support**: Easy deployment with Docker and docker-compose

## Requirements

- Python 3.11+
- UV package manager
- Docker (optional, for containerized deployment)

## Setup

### 1. Get a Bot Token

1. Talk to [@BotFather](https://t.me/BotFather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token

### 2. Configure the Bot

Copy the example environment file and add your bot token:

```bash
cp .env.example .env
# Edit .env and add your BOT_TOKEN
```

### 3. Installation

#### Using UV (Local Development)

```bash
# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -e .

# Run the bot
python -m bot
```

#### Using Docker Compose (Recommended for Production)

**Note**: Docker build requires internet access to download dependencies from PyPI.

```bash
# Build and run the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

If you encounter SSL certificate errors during Docker build, you can use the pre-built image approach or run locally with UV.

## Bot Setup in Telegram

1. **Add the bot to your channel's discussion group**
   - Open your channel's discussion group
   - Add the bot as a member

2. **Make the bot an admin**
   - Go to group settings → Administrators
   - Add the bot as an administrator
   - Enable "Delete messages" permission

3. **Configure the bot**
   - Send `/start` in the group to initialize the bot
   - The bot will automatically detect the linked channel

## Commands

- `/start` - Initialize the bot and show welcome message
- `/config` - View current configuration
- `/status` - Check bot status and permissions
- `/enable` - Enable spam filtering (admin only)
- `/disable` - Disable spam filtering (admin only)

## How It Works

1. The bot monitors all messages in the discussion group
2. When a message contains links:
   - If the user is an admin → message is allowed
   - If the link is to the connected channel → message is allowed
   - Otherwise → message is deleted
3. Admins can configure the bot using commands in the group

## Configuration

Environment variables in `.env`:

- `BOT_TOKEN` - Your Telegram bot token (required)
- `LOG_LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)

## Development

### Project Structure

```
telegram-antispam/
├── bot/
│   ├── __init__.py
│   ├── __main__.py      # Main entry point
│   ├── config.py        # Configuration management
│   ├── filters.py       # Message filtering logic
│   ├── handlers.py      # Command and message handlers
│   └── storage.py       # Configuration storage
├── .env.example         # Example environment file
├── .gitignore
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile           # Docker image definition
├── LICENSE
├── pyproject.toml       # Project dependencies
└── README.md
```

### Running Locally

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with UV
uv pip install -e .

# Run the bot
python -m bot
```

## License

MIT License - see [LICENSE](LICENSE) file for details
