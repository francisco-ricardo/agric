FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
