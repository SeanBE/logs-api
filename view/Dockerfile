FROM ubuntu:14.04
MAINTAINER Sean Löfgren "lofgren.sean@gmail.com"

RUN apt-get update
RUN apt-get -y install apache2

ENV INSTALL_PATH /var/www/html/
WORKDIR $INSTALL_PATH
ADD . $INSTALL_PATH
