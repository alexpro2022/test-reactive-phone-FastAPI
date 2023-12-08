FROM python:3.11-slim
WORKDIR /app
COPY requirements .
RUN python -m pip install --upgrade pip && \
    pip install -r dev.requirements.txt --no-cache-dir
COPY . .
