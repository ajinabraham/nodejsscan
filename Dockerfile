FROM postgres:12.3
LABEL authors="Ajin Abraham <ajin25@gmail.com>" \
   description="nodejsscan is a static security code scanner for Node.js applications."


ENV POSTGRES_USER root
ENV POSTGRES_PASSWORD root
ENV POSTGRES_DB nodejsscan


WORKDIR /usr/src/nodejsscan
COPY requirements.txt .

RUN apt update -y && apt install -y \
   git \
   python3.7 \
   python3-pip && \
   pip3 install --quiet --no-cache-dir -r requirements.txt && \
   apt clean && \
   apt autoclean && \
   apt autoremove -y && \
   rm -rf /var/lib/apt/lists/* /tmp/* > /dev/null 2>&1

COPY . .

EXPOSE 9090

CMD ["sh","entrypoint.sh"]