# Copilot Instructions for telegram-antispam

This repository contains a Telegram bot for filtering spam in channel discussion groups using Python and the aiogram framework.

## Project Overview

**telegram-antispam** is a Telegram bot that:
- Automatically filters messages containing external links in channel discussion groups
- Allows admins and channel posts to bypass filtering
- Supports both polling and webhook modes
- Uses in-memory configuration storage (production should use a database)

## Technology Stack

- **Language**: Python 3.11+
- **Framework**: aiogram 3.15.0+ (async Telegram bot framework)
- **Package Manager**: UV (fast Python package installer)
- **Deployment**: Docker and Docker Compose
- **Dependencies**: python-dotenv for environment configuration

## Project Structure

```
telegram-antispam/
├── bot/
│   ├── __init__.py       # Package initialization
│   ├── __main__.py       # Entry point with polling/webhook modes
│   ├── config.py         # Environment configuration
│   ├── filters.py        # Link detection & filtering logic
│   ├── handlers.py       # Command & message handlers
│   └── storage.py        # In-memory configuration storage
├── .env.example          # Environment template
├── Dockerfile            # Container image
├── docker-compose.yml    # Orchestration
└── pyproject.toml        # Dependencies & build config
```

## Key Components

### 1. Configuration (`config.py`)
- Loads environment variables using `python-dotenv`
- Required: `BOT_TOKEN` from @BotFather
- Optional: `LOG_LEVEL`, webhook configuration
- Validates required settings on startup

### 2. Filters (`filters.py`)
- `extract_links()`: Detects URLs, @mentions, and t.me links
- `is_link_to_channel()`: Validates if link points to allowed channel
- `should_delete_message()`: Main filtering decision logic
- `is_user_admin()`: Checks admin permissions
- `get_linked_channel()`: Retrieves connected channel info

### 3. Handlers (`handlers.py`)
- `/start`: Welcome message and setup instructions
- `/config <chat_id>`: View/update configuration (private chat only)
- `/status`: Check bot status and permissions
- `/enable`: Enable filtering (admin only)
- `/disable`: Disable filtering (admin only)
- Message handler: Filters all incoming messages based on rules

### 4. Storage (`storage.py`)
- In-memory dictionary for chat configurations
- ChatConfig dataclass with `enabled` and `allowed_channel_username` fields
- Simple get/set interface
- **Note**: Not persistent, resets on restart

## Coding Standards

### Python Style
- Follow PEP 8 conventions
- Use type hints for function parameters and return values
- Use async/await for all I/O operations (aiogram is async)
- Keep functions focused and single-purpose
- Use descriptive variable names

### Error Handling
- Use try-except blocks for external API calls (Telegram API)
- Log errors with appropriate levels (ERROR, WARNING, INFO, DEBUG)
- Gracefully handle permission errors and user errors
- Don't expose sensitive information in error messages

### Documentation
- Use docstrings for all public functions and classes
- Keep README.md and IMPLEMENTATION.md up to date
- Document environment variables in .env.example
- Add inline comments for complex logic only

## Development Workflow

### Local Development
```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Configure environment
cp .env.example .env
# Edit .env and add your BOT_TOKEN

# Run the bot
python -m bot
```

### Testing
- Test with a real Telegram bot in a test group
- Verify link detection with various URL formats
- Test admin permissions and command access
- Validate both polling and webhook modes
- Check error handling with invalid configurations

### Docker Development
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

## Important Considerations

### Telegram Bot Specifics
- Bot must be added to the channel's discussion group
- Bot requires "Delete messages" admin permission
- Use `sender_chat` to detect messages from the channel itself
- Admin checks are chat-specific (user can be admin in one chat but not another)

### Webhook vs Polling
- **Polling** (default): Bot actively requests updates from Telegram
  - Easier to set up, works anywhere
  - Uses long polling with timeout
  - Default mode if `WEBHOOK_MODE` is not set or false
  
- **Webhook**: Telegram pushes updates to your server
  - More efficient for high-volume bots
  - Requires public HTTPS URL and reverse proxy (nginx)
  - Configure with `WEBHOOK_MODE=true` and related env vars
  - Runs aiohttp web server on specified port

### Security
- Never commit BOT_TOKEN or sensitive data to git
- Validate admin permissions before executing privileged commands
- Use webhook secret token for webhook security
- Only respond to commands from admins in groups

### Configuration Storage
- Current implementation uses in-memory storage (not persistent)
- For production, consider implementing database storage
- Per-chat configuration with chat_id as key
- Auto-detects linked channel on /start or /config

## Common Tasks

### Adding a New Command
1. Add handler function in `bot/handlers.py`
2. Use `@router.message(Command("commandname"))` decorator
3. Check admin permissions if needed with `is_user_admin()`
4. Update README.md with command documentation

### Modifying Link Detection
1. Update `extract_links()` in `bot/filters.py`
2. Add regex patterns or parsing logic
3. Test with various link formats
4. Consider edge cases (malformed URLs, Unicode, etc.)

### Adding New Configuration Options
1. Update `ChatConfig` dataclass in `bot/storage.py`
2. Add getter/setter logic if needed
3. Update `/config` command to display new options
4. Document in README.md and .env.example if environment-based

### Deployment
- Use pre-built images from `ghcr.io/yurzs/telegram-antispam:latest`
- Tag releases with version numbers (e.g., v1.0.0) to trigger CI/CD
- GitHub Actions automatically builds and publishes Docker images
- Update docker-compose.yml for webhook port exposure if needed

## Resources

- aiogram documentation: https://docs.aiogram.dev/
- Telegram Bot API: https://core.telegram.org/bots/api
- UV documentation: https://github.com/astral-sh/uv
- Python asyncio: https://docs.python.org/3/library/asyncio.html

## AI Assistant Guidelines

When helping with this project:
- Maintain async/await patterns throughout the codebase
- Preserve the simplicity of in-memory storage unless database migration is explicitly requested
- Follow existing code structure and naming conventions
- Test changes with different Telegram message types and user permissions
- Consider both polling and webhook modes when making changes to the main entry point
- Update documentation when adding new features or changing behavior
- Keep the bot lightweight and focused on spam filtering
