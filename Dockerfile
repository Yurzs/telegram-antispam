FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy project files
COPY pyproject.toml ./
COPY bot ./bot

# Install dependencies using uv
RUN uv pip install --system --no-cache aiogram>=3.15.0 python-dotenv>=1.0.0

# Expose webhook port (default 8080, can be overridden with WEBHOOK_PORT env var)
EXPOSE 8080

# Run the bot
CMD ["python", "-m", "bot"]
