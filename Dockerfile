FROM postgres:9.6.2-alpine

LABEL authors="Cristobal Infantes <cristobal.infantes@gmail.com>" \
	  maintainer="Ajin Abraham <ajin25@gmail.com>" \
	  description="Static Security Code Scanner for Node.js Applications"

EXPOSE 9090

ENV POSTGRES_USER root
ENV POSTGRES_DB nodejsscan

RUN cd /usr/src \
 && apk add --update \
    python3 \
    python3-dev \
    build-base \
    git \
 && python3 -m ensurepip \
 && git clone https://github.com/ajinabraham/NodeJsScan.git \
 && cd NodeJsScan \
 && sed -i -e s/postgresql:\\/\\/localhost\\/nodejsscan/postgresql:\\/\\/127.0.0.1\\/nodejsscan/g core/settings.py \
 && pip3 install -r requirements.txt \
 && apk del python3-dev \
    build-base \
    git \
 && rm -rf /var/cache/apk/*

ADD start.sh /usr/src/NodeJsScan
WORKDIR /usr/src/NodeJsScan
CMD ["sh","/usr/src/NodeJsScan/start.sh"]
