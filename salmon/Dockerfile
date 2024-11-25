FROM ubuntu:eoan-20200114

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get dist-upgrade -y \
    && apt-get install -y --no-install-recommends\
        autoconf \
        bzip2 \
        cmake \
        curl \
        gcc \
        g++ \
        libboost-all-dev \
        libbz2-dev \
        liblzma5 \
        liblzma-dev \
        libcurl4 \
        libcurl4-openssl-dev \
        libjemalloc2 \
        libjemalloc-dev \
        make \
        python3-pkgconfig \
        wget \
        unzip \
        zlib1g \
        zlib1g-dev \
    && apt-get clean \
    && wget --no-check-certificate https://github.com/COMBINE-lab/salmon/archive/v1.0.0.tar.gz \
    && tar xf v1.0.0.tar.gz \
    && cd salmon-1.0.0/ \
    && mkdir build \
    && cd build/ \
    && cmake .. \
    && make \
    && make install \
    && cd ../../ \
    && rm -rf salmon* v1.0.0.tar.gz \
    && apt-get remove --purge -y \
        autoconf \
        cmake \
        curl \
        gcc \
        g++ \
        libbz2-dev \
        liblzma-dev \
        make \
        wget \
        unzip \
        zlib1g-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
