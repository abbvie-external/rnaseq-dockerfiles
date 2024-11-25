FROM ubuntu:noble-20240605

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

COPY picard-metrics-sqlite/ /picard-metrics-sqlite/

RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y \
       python3-pandas \
       python3-pip \
       python3-sqlalchemy \
    && pip3 install picard-metrics-sqlite/ --break-system-packages \
    && apt-get clean \
    && apt-get remove --purge -y \
       python3-dev \
       python3-pip \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
