FROM python:2.7-slim
MAINTAINER John Doe <jdoe@Jupiter.local.net>

ENV INSTALL_PATH /application

ADD . $INSTALL_PATH
WORKDIR $INSTALL_PATH
RUN pip install -r requirements.txt

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "snakeeyes.app:create_app()"
