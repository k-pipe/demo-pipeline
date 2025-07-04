FROM python:3.10-slim-bullseye
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app /app
WORKDIR /app
ENTRYPOINT ["python3", "-u", "/app/main.py"]
