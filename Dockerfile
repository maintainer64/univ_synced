FROM python:3.8-slim
WORKDIR /opt/app
COPY requirements.txt .
RUN pip install --upgrade pip -r requirements.txt
COPY . .
