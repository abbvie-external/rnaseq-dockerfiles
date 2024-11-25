FROM ubuntu:noble-20240605

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

COPY qualimap-sqlite /qualimap-sqlite/

RUN apt-get update && apt-get dist-upgrade -y \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y \
       python3-pandas \
       python3-pip \
       python3-sqlalchemy \
    && apt-get clean \
    && pip3 install qualimap-sqlite/ --break-system-packages \
    && apt-get remove --purge -y \
       python3-pip \
       python3-dev \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
