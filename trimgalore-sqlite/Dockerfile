FROM ubuntu:jammy-20221130

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

COPY trimgalore-sqlite /trimgalore-sqlite/

RUN apt-get update && apt-get dist-upgrade -y \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y \
       python3-pandas \
       python3-pip \
       python3-sqlalchemy \
    && apt-get clean \
    && pip3 install trimgalore-sqlite/ \
    && apt-get remove --purge -y \
       binutils \
       ca-certificates \
       cpp \
       dpkg-dev \
       libc6-dev \
       python3-pip \
       x11-common \
       xdg-user-dirs \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
