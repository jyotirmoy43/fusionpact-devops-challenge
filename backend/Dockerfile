
FROM python:3.9-slim

WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source
COPY ./app ./app

# Run the FastAPI app
CMD ["python", "app/main.py"]

