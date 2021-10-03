FROM python:2.7.15-alpine3.7
MAINTAINER MrSea

RUN apk --update add build-base linux-headers pcre-dev libjpeg zlib tiff-dev freetype-dev make libressl-dev py2-pip libffi-dev gettext gcc libpq netcat-openbsd libxml2-dev zlib-dev libxslt-dev ca-certificates musl-dev python-dev libre2-dev g++ && rm -rf /var/cache/apk/*
RUN pip --no-cache-dir install --upgrade pip setuptools

RUN mkdir -p /webapps
WORKDIR /webapps/inside

##### These 2 steps make build faster
ADD requirements.txt ./
RUN pip install -r requirements.txt
#####

ADD . ./

RUN chmod 775 start.sh
ENTRYPOINT ["/webapps/inside/start.sh"]
CMD []
