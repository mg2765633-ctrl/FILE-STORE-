FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install the required python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bot's source code
COPY . .

# Make your start script executable
RUN chmod +x start.sh

# Start the bot using your shell script
CMD ["bash", "start.sh"]
