FROM ubuntu:noble-20240605

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

COPY integrity-to-sqlite /integrity-to-sqlite/

RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get upgrade --no-install-recommends -y \
    && apt-get install --no-install-recommends -y \
        python3 \
        python3-pandas \
        python3-pip \
        python3-setuptools \
        python3-sqlalchemy \
    && apt-get clean \
    && pip3 install integrity-to-sqlite/ --break-system-packages \
    && apt-get remove --purge -y \
       python3-pip \
       python3-setuptools \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
