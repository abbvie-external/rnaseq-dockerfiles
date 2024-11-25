FROM ubuntu:jammy-20221130

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install -y \
       samtools \
    && apt-get clean \
    && apt-get autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
