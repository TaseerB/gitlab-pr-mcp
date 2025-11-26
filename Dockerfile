FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the server
CMD ["python", "server.py"]
