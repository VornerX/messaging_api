FROM python:3.11-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /usr/messaging_api

COPY messaging_api messaging_api
COPY requirements.txt /usr/messaging_api

RUN apt-get update && apt-get install -y --no-install-recommends  \
    build-essential python3-dev -y \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install -U pip \
    && pip install -U wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m compileall messaging_api

EXPOSE 8000

CMD ["uvicorn", "messaging_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
