FROM ubuntu:focal-20200423

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \ 
        gcc \
        libbz2-1.0 \
        libbz2-dev \
        liblzma5 \
        liblzma-dev \
        make \
        python3-dev \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        unzip \
        wget \
        zlib1g \
        zlib1g-dev \
    && apt-get clean \
    && pip3 install cython \
    && pip3 install RSeQC \
    && apt-get remove --purge -y \
        gcc \
        libbz2-dev \
        liblzma-dev \
        python3-dev \
        make \
        unzip \
        wget \
        zlib1g-dev \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
