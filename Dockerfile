FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY bot ./bot

# Install dependencies directly (without editable mode to avoid build requirements)
RUN pip install --no-cache-dir aiogram>=3.15.0 python-dotenv>=1.0.0

# Run the bot
CMD ["python", "-m", "bot"]
