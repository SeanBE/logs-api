FROM python:3.5-slim

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    netcat \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV INSTALL_PATH /application
WORKDIR $INSTALL_PATH
ADD requirements.txt $INSTALL_PATH
RUN pip install -r requirements.txt
ADD . $INSTALL_PATH
