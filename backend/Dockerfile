FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port your app runs on
EXPOSE 5000

# Command to run your app
CMD ["python", "app/app.py"]

