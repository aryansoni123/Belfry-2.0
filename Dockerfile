# Dockerfile for Belfry Flask Application
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Initialize the database (SQLite by default)
RUN python init_db.py --seed

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
