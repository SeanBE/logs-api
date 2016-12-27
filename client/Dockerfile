FROM nginx:alpine
MAINTAINER Sean Löfgren "lofgren.sean@gmail.com"

RUN apk update
RUN apk add nodejs

ADD . /tmp/
WORKDIR /tmp

RUN npm install
RUN npm run build

RUN mv config/nginx.conf /etc/nginx/conf.d/default.conf
RUN mv dist/* /usr/share/nginx/html
