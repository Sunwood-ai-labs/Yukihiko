# Dockerfile
FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y git

# Git設定をDockerfile内で行う
RUN git config --global user.email 'yukihiko.fuyuki@gmail.com' && \
    git config --global user.name 'Yukihiko'

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
