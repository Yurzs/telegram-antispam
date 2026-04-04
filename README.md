# telegram-antispam

Telegram bot for filtering channel comments and preventing spam in discussion groups.

## Features

- 🛡️ **Automatic spam filtering**: Detects and removes messages with external links
- 🔗 **Advanced link detection**: Detects URLs with or without protocol (https://, t.co/xyz, bit.ly/abc), formatted links in HTML/Markdown, @mentions, and private channel links (t.me/c/{id})
- ✅ **Channel integration**: Automatically allows links to the connected channel (both username and ID-based links) and current chat
- 👮 **Admin-friendly**: Admins can post any links without restrictions; non-admins' commands are silently ignored
- 📬 **Admin notifications**: Deleted messages are forwarded to admins via private message for review
- ⚙️ **Easy configuration**: Simple commands to manage the bot
- 🔄 **Polling & Webhook support**: Choose between polling mode or webhook mode for receiving updates
- 🔒 **Proxy support**: Route Telegram API traffic through a SOCKS5/SOCKS4/HTTP proxy
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

**Using Pre-built Image from GitHub Container Registry:**

```bash
# Pull and run the latest image
docker pull ghcr.io/yurzs/telegram-antispam:latest

# Or use docker-compose (update docker-compose.yml to use the pre-built image)
docker-compose up -d
```

**Building Locally:**

```bash
# Build and run the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

**Note**: Pre-built images are automatically published to GitHub Container Registry when you create a new version tag (e.g., `v1.0.0`). You can also build locally if needed.

#### Using Webhook Mode (Advanced)

For production deployments with webhook mode:

1. **Set up a reverse proxy (e.g., nginx with SSL)**
2. **Configure environment variables:**
   ```bash
   # In your .env file
   BOT_TOKEN=your_bot_token_here
   WEBHOOK_MODE=true
   WEBHOOK_HOST=https://yourdomain.com
   WEBHOOK_PATH=/webhook
   WEBHOOK_PORT=8080
   WEBHOOK_SECRET=your_random_secret_token
   ```

3. **Update docker-compose.yml to expose the webhook port:**
   ```yaml
   services:
     bot:
       image: ghcr.io/yurzs/telegram-antispam:latest
       env_file:
         - .env
       restart: unless-stopped
       ports:
         - "8080:8080"  # Expose webhook port
   ```

4. **Configure nginx as reverse proxy:**
   ```nginx
   server {
       listen 443 ssl;
       server_name yourdomain.com;
       
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;
       
       location /webhook {
           proxy_pass http://localhost:8080/webhook;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

5. **Start the bot:**
   ```bash
   docker-compose up -d
   ```

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
   - If the message is from the linked channel itself (via `sender_chat`) → message is allowed ✅
   - If the user is an admin → message is allowed ✅
   - If the link is to the connected channel → message is allowed ✅
   - Otherwise → message is deleted ❌
3. **Admins can configure the bot using commands in private chat**

### Example Scenarios

**Scenario 1: Channel posts to its discussion group**
```
Channel: "New article published! https://example.com/article"
Bot: ✅ Allowed (message from linked channel)
```

**Scenario 2: Regular user posts a link to the connected channel**
```
User: "Check out our latest post! https://t.me/mychannel/123"
Bot: ✅ Allowed (link to connected channel)
```

**Scenario 3: Regular user posts an external link**
```
User: "Visit https://spam-site.com for prizes!"
Bot: ❌ Deleted (external link from non-admin)
```

**Scenario 4: Admin posts any link**
```
Admin: "Here's a useful resource: https://example.com"
Bot: ✅ Allowed (admin user)
```

## Configuration

Environment variables in `.env`:

- `BOT_TOKEN` - Your Telegram bot token (required)
- `LOG_LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)

### Proxy Configuration (Optional)

The bot supports routing all Telegram API requests through a SOCKS5 (or SOCKS4/HTTP) proxy:

- `PROXY_URL` - Proxy URL (e.g., `socks5://user:password@host:port`, `socks5://host:port`)

This is useful when deploying in environments where direct access to the Telegram API is restricted.

### Webhook Configuration (Optional)

The bot supports both **polling** (default) and **webhook** modes:

- `WEBHOOK_MODE` - Set to `true` to enable webhooks, `false` for polling (default: false)
- `WEBHOOK_HOST` - Your public webhook URL (required if WEBHOOK_MODE=true, e.g., `https://yourdomain.com`)
- `WEBHOOK_PATH` - Webhook endpoint path (default: `/webhook`)
- `WEBHOOK_PORT` - Port for the webhook server (default: `8080`)
- `WEBHOOK_SECRET` - Secret token for webhook security (optional but recommended)

**Polling vs Webhook:**
- **Polling** (default): Bot actively checks for new messages. Easier to set up, works anywhere.
- **Webhook**: Telegram sends updates to your server. More efficient, requires public HTTPS URL and port forwarding/reverse proxy.

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
