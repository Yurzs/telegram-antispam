# Copilot Instructions for telegram-antispam

## Project Overview
This is a Telegram bot designed for filtering channel comments. The bot helps moderate comments in Telegram channels by detecting and filtering spam or inappropriate content.

## Technology Stack
- **Primary Language**: Python
- **Platform**: Telegram Bot API
- **Purpose**: Anti-spam and content moderation

## Coding Standards

### Python Style
- Follow PEP 8 style guidelines
- Use type hints where applicable
- Write clear, descriptive variable and function names
- Add docstrings to all public functions and classes

### Code Organization
- Keep functions focused and single-purpose
- Use meaningful module and file names
- Organize imports: standard library, third-party, local

### Error Handling
- Use specific exception types rather than bare except clauses
- Log errors appropriately for debugging
- Handle Telegram API errors gracefully

## Best Practices

### Security
- Never commit API tokens or sensitive credentials
- Use environment variables for configuration
- Validate and sanitize user input

### Testing
- Write unit tests for core functionality
- Test edge cases and error conditions
- Mock external API calls in tests

### Documentation
- Update README.md when adding new features
- Document configuration options
- Provide setup instructions for new contributors

## Common Patterns
- Use async/await for Telegram bot operations
- Implement proper logging for debugging and monitoring
- Follow the bot's command pattern for new features
