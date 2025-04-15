FROM python:3.10-alpine
COPY . /app
WORKDIR /app
RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8080
