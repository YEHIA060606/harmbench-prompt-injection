# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory if not exists
RUN mkdir -p data

# Default command (run full pipeline)
CMD ["python", "src/02_run_models.py"]