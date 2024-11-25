FROM debian:sid

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \ 
       r-bioc-tximport \
       r-bioc-tximportdata \
    && apt-get clean \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
