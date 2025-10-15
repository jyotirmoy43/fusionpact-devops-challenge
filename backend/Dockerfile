FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy code directly into /app (not /app/app)
COPY ./app/* ./

CMD ["python", "main.py"]


