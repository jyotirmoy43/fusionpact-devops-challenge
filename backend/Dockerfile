FROM python:3.9-slim

WORKDIR /app

# Copy dependency file and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend app
COPY ./app ./app

# Set the working directory to where main.py lives
WORKDIR /app/app

# Run FastAPI using Uvicorn
CMD ["python", "main.py"]



