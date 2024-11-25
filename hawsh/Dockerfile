FROM ubuntu:jammy-20240627.1

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG hawshversion=v1.0.1
ARG kallistoversion=0.44.0
ARG rseqcversion=4.0.0

COPY check_strandedness.diff /

RUN apt-get update -y --allow-unauthenticated --allow-insecure-repositories \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --allow-unauthenticated \
       autoconf \
       cmake \
       gcc \
       g++ \
       libbz2-1.0 \
       libbz2-dev \
       libhdf5-cpp-103-1 \
       libhdf5-dev \
       liblzma5 \
       liblzma-dev \
       make \
       python3-pandas \
       python3-pip \
       wget \
       unzip \
    && wget https://github.com/pachterlab/kallisto/archive/refs/tags/v$kallistoversion.tar.gz \
    && wget -O RSeQC-$rseqcversion.tar.gz https://sourceforge.net/projects/rseqc/files/RSeQC-$rseqcversion.tar.gz/download \
    && wget https://github.com/signalbash/how_are_we_stranded_here/archive/refs/heads/master.zip \
    && tar xf v$kallistoversion.tar.gz \
    && cd kallisto-$kallistoversion \
    && cd ext/htslib/ \
    && autoreconf --install \
    && ./configure --host=x86_64 --target=x86_64 \
    && cd ../../ \
    && sed -i 's/disable-libcurl/disable-libcurl --host=x86_64/g' CMakeLists.txt \
    && sed -i '/^#include <algorithm>/a #include <limits>' /kallisto-0.44.0/src/MinCollector.cpp \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make \
    && make install \
    && cd ../../ \
    && rm -rf kallisto* v$kallistoversion.tar.gz \
    && pip install RSeQC==4.0.0 \
    && unzip master.zip \
    && cd how_are_we_stranded_here-master/ \
    && patch -p1 < ../check_strandedness.diff \
    && cd ../ \
    && pip install ./how_are_we_stranded_here-master/ \
    && rm master.zip \
    && rm -rf how_are_we_stranded_here-master/ \
    && rm RSeQC-$rseqcversion.tar.gz \
    && apt-get clean \
    && apt-get remove -y --purge \
       autoconf \
       cmake \
       gcc \
       g++ \
       libbz2-dev \
       libhdf5-dev \
       liblzma-dev \
       make \
       python3-pip \
       wget \
       unzip \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
