FROM python:3.10-alpine
WORKDIR /app
COPY . /app
RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt
ENV PYTHONPATH=/app/src
EXPOSE 8080
