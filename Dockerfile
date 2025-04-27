FROM python:3.10-alpine AS base
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY src /app
COPY path_definitions.py /app

FROM base AS dev
COPY requirements-dev.txt .
RUN python3 -m pip install --upgrade pip && pip install --no-cache-dir -r requirements-dev.txt
COPY tests /app
COPY pytest.ini /app

FROM base AS prod

FROM dev AS test


#ENV PYTHONPATH=/app/src
#EXPOSE 8080
