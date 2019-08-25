FROM postgres:9.6.2-alpine
LABEL authors="Cristobal Infantes <cristobal.infantes@gmail.com>" \
   maintainer="Ajin Abraham <ajin25@gmail.com>" \
   description="Static Security Code Scanner for Node.js Applications"
EXPOSE 9090
ENV POSTGRES_USER root
ENV POSTGRES_DB nodejsscan
WORKDIR /usr/src/NodeJsScan
COPY requirements.txt requirements.txt
COPY ./core/settings.py ./core/settings.py
RUN apk add --no-cache \
   python3=3.5.6-r0 \
   python3-dev=3.5.6-r0 \
   build-base=0.4-r1 \
   && python3 -m ensurepip \
   && sed -i -e s/postgresql:\\/\\/localhost\\/nodejsscan/postgresql:\\/\\/127.0.0.1\\/nodejsscan/g core/settings.py \
   && pip3 install -r requirements.txt \
   && apk del python3-dev build-base
COPY . .
CMD ["sh","start.sh"]