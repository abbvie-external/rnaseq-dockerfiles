FROM ubuntu:focal-20240530

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG genversion=1.12.0
ARG gffversion=v0.12.0

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        python3-minimal \
        python3-pip \
        python3-setuptools \
        unzip \
        wget \
        zlib1g \
        zlib1g-dev \
    && apt-get clean \
    && wget https://github.com/fls-bioinformatics-core/genomics/archive/$genversion.tar.gz \
    && wget https://github.com/fls-bioinformatics-core/GFFUtils/archive/$gffversion.tar.gz \
    && pip install $genversion.tar.gz \
    && pip install $gffversion.tar.gz \
    && rm *.tar.gz \
    && apt-get remove --purge -y \
         ca-certificates \
         python3-pip \
         python3-setuptools \
         unzip \
         wget \
         zlib1g-dev \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
