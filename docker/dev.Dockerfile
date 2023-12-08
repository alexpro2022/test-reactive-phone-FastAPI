FROM python:3.11-slim
WORKDIR /app
COPY requirements .
RUN python -m pip install --upgrade pip && \
    pip install -r test.requirements.txt --no-cache-dir
COPY . .
# CMD alembic upgrade head && uvicorn app.main:app --host=0.0.0.0
