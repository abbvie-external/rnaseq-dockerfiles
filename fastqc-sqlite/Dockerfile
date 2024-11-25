FROM ubuntu:noble-20240605

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

COPY fastqc-sqlite/ /fastqc-sqlite/

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
    && pip3 install fastqc-sqlite/ --break-system-packages \
    && rm -rf fastqc-sqlite \
    && apt-get remove --purge -y \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        zlib1g-dev \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
