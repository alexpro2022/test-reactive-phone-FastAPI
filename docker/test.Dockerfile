FROM python:3.11-slim
WORKDIR /app
COPY requirements .
RUN python -m pip install --upgrade pip && \
    pip install -r test.requirements.txt --no-cache-dir
COPY . .
ENV DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
ENV REDIS_URL=redis://redis:6379
CMD coverage run --source=app -m pytest && coverage report -m
