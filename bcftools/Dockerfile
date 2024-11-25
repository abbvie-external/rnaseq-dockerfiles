FROM ubuntu:noble-20240605

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install -y \
        bcftools \
        tabix \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
