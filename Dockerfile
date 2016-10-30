FROM python:2.7-slim
MAINTAINER John Doe <jdoe@Jupiter.local.net>

ENV INSTALL_PATH /application
WORKDIR $INSTALL_PATH
ADD requirements.txt $INSTALL_PATH
RUN pip install -r requirements.txt
ADD . $INSTALL_PATH

EXPOSE 5000
CMD python server.py
