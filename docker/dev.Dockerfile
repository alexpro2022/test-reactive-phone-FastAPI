FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir
COPY . .
# CMD alembic upgrade head && uvicorn app.main:app --host=0.0.0.0
