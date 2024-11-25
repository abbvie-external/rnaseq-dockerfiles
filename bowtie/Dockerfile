FROM ubuntu:mantic-20240122

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \ 
        bowtie \
    && apt-get clean \
    && apt-get autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ /tmp/* /var/tmp/*
