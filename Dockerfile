FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port (Fly.io defaults to 8080 usually, but we can set 8000)
EXPOSE 8000

# Run Uvicorn backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
