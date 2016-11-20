FROM python:2.7-slim
MAINTAINER Sean Lofgren <lofgren.sean@gmail.com>

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

EXPOSE 5000
CMD python server.py
