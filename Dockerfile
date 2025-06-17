FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "agric.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
