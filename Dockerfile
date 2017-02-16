FROM ubuntu:16.04

MAINTAINER Ajin Abraham <ajin25@gmail.com>

# Update the repository sources list
RUN apt-get update -y

#Postgres Installation
RUN apt-get install -y \
    postgresql \
    postgresql-contrib

#Install Git and required Libs
RUN apt-get install -y \
    git \
    build-essential \
    libpq-dev

#Install Python, pip
RUN \
  apt-get install -y \
  python \
  python-dev \
  python-pip && \
  pip install --upgrade pip

#Cleanup
RUN \
  rm -rf /var/lib/apt/lists/*

#Clone NodeJsScan master
WORKDIR /root
RUN git clone https://github.com/ajinabraham/NodeJsScan.git

#Enable Virtualenv and Install Dependencies
WORKDIR /root/NodeJsScan

RUN pip install -r requirements.txt

#Expose NodeJsScan Port
EXPOSE 9090

#Create Tables Entries
WORKDIR /root/NodeJsScan
CMD ["python","createdb.py"]

#Run NodeJsScan
CMD ["python","app.py"]