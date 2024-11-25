FROM ubuntu:mantic-20240530

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG version=2.7.11b

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \ 
        gcc \
        g++ \
        libgomp1 \
        make \
        wget \
        xxd \
        zlib1g \
        zlib1g-dev \
    && apt-get clean \
    && wget --no-check-certificate https://github.com/alexdobin/STAR/archive/$version.tar.gz \
    && tar xf $version.tar.gz \
    && rm $version.tar.gz \
    && cd STAR-$version/source \
    && make STAR \
    && mv STAR /usr/local/bin/ \
    && cd ../../ \
    && rm -rf STAR-$version \
    && apt-get remove --purge -y \
        gcc \
        g++ \
        make \
        wget \
        xxd \
        zlib1g-dev \
    && apt-get autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ /tmp/* /var/tmp/*
