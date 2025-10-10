# telegram-antispam

Telegram bot for filtering channel comments and preventing spam in discussion groups.

## Features

- 🛡️ **Automatic spam filtering**: Detects and removes messages with external links
- ✅ **Channel integration**: Automatically allows links to the connected channel
- 👮 **Admin-friendly**: Admins can post any links without restrictions
- ⚙️ **Easy configuration**: Simple commands to manage the bot
- 🐳 **Docker support**: Easy deployment with Docker and docker-compose
- 📦 **UV package manager**: Fast, reliable dependency management with UV

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
   - Send `/status` in the group to get the chat ID
   - Start a private chat with the bot and send `/start`
   - Use `/config <chat_id>` in the private chat to view/configure settings
   - The bot will automatically detect the linked channel

## Commands

- `/start` - Initialize the bot and show welcome message
- `/status` - Check bot status and get chat ID (use in group)
- `/config <chat_id>` - View/change configuration (use in private chat with bot)
- `/enable` - Enable spam filtering (admin only, use in group)
- `/disable` - Disable spam filtering (admin only, use in group)

## How It Works

1. **The bot monitors all messages in the discussion group**
2. **When a message contains links:**
   - If the user is an admin → message is allowed ✅
   - If the link is to the connected channel → message is allowed ✅
   - Otherwise → message is deleted ❌
3. **Admins can configure the bot using commands in the group**

### Example Scenarios

**Scenario 1: Regular user posts a link to the connected channel**
```
User: "Check out our latest post! https://t.me/mychannel/123"
Bot: ✅ Allowed (link to connected channel)
```

**Scenario 2: Regular user posts an external link**
```
User: "Visit https://spam-site.com for prizes!"
Bot: ❌ Deleted (external link from non-admin)
```

**Scenario 3: Admin posts any link**
```
Admin: "Here's a useful resource: https://example.com"
Bot: ✅ Allowed (admin user)
```

## Configuration

Environment variables in `.env`:

- `BOT_TOKEN` - Your Telegram bot token (required)
- `LOG_LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)

## Development

### Quick Start Example

1. **Create your bot**:
   ```bash
   # Talk to @BotFather and get your token
   # Then set it up:
   cp .env.example .env
   # Edit .env and add: BOT_TOKEN=your_token_here
   ```

2. **Run locally**:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   python -m bot
   ```

3. **Add to your Telegram channel**:
   - Add the bot to your channel's discussion group
   - Make it an admin with "Delete messages" permission
   - Send `/status` in the group to get the chat ID
   - Use `/config <chat_id>` in private chat with the bot

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
