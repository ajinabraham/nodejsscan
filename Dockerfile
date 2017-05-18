FROM postgres:9.6.2-alpine

LABEL authors="Cristobal Infantes <cristobal.infantes@gmail.com>"

EXPOSE 9090

ENV POSTGRES_USER root
ENV POSTGRES_DB nodejsscan

RUN cd /usr/src \
 && apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
    git \
 && git clone https://github.com/ajinabraham/NodeJsScan.git \
 && cd NodeJsScan \
 && sed -i -e s/postgresql:\\/\\/localhost\\/nodejsscan/postgresql:\\/\\/127.0.0.1\\/nodejsscan/g core/settings.py \
 && pip install -r requirements.txt \
 && apk del python-dev \
    build-base \
    git \
 && rm -rf /var/cache/apk/*

ADD start.sh /usr/src/NodeJsScan
WORKDIR /usr/src/NodeJsScan
CMD ["sh","start.sh"]