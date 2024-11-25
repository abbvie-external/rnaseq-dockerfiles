FROM ubuntu:jammy-20221130

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

COPY star-sqlite /star-sqlite/

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \ 
       python3-pandas \
       python3-pip \
       python3-setuptools \
       python3-sqlalchemy \
       python3-wheel \
       zlib1g \
       zlib1g-dev \
    && apt-get clean \
    && pip3 install star-sqlite/ \
    && apt-get remove --purge -y \
       ca-certificates \
       libc6-dev \
       openssl \
       python3-pip \
       python3-setuptools \
       python3-wheel \
       zlib1g-dev \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
