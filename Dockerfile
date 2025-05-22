FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y \
        git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt ./main.py ./alembic.ini /app/

RUN pip install --upgrade pip && \
	pip install --no-cache-dir -r /app/requirements.txt

COPY ./.keys/ /app/.keys
COPY ./docker /app/docker
COPY ./alembic /app/alembic
COPY ./app/ /app/app

HEALTHCHECK --interval=45s --timeout=3s \
    CMD curl -f http://localhost:8000/ || exit 1

RUN ["chmod", "+x", "/app/docker/backend/asgi-entrypoint.sh"]
ENTRYPOINT [ "/app/docker/backend/asgi-entrypoint.sh" ]

EXPOSE 8000
