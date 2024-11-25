FROM ubuntu:oracular-20240527

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG version=0.8.3.post1

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pandas \
        python3-pip \
        python3-pillow \
        python3-matplotlib \
        python3-numpy \
        python3-scipy \
        python3-sklearn \
        zlib1g \
    && apt-get clean \
    && pip3 install --break-system-packages zpca==$version \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
