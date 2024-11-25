FROM ubuntu:eoan-20200114

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \ 
        gcc \
        g++ \
        make \
        r-base-core \
        wget \
        zlib1g \
        zlib1g-dev \
    && Rscript -e 'install.packages("BiocManager"); \
        BiocManager::install(update = TRUE, ask = FALSE); \
        BiocManager::install(c("limma"));' \
    && apt-get clean \
    && apt-get remove --purge -y \
        gcc \
        g++ \
        make \
        wget \
        zlib1g-dev \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
