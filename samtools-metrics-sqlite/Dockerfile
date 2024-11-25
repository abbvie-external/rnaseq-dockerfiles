FROM ubuntu:jammy-20221130

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

COPY samtools-metrics-sqlite /samtools-metrics-sqlite/

RUN apt-get update && apt-get dist-upgrade -y \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y \
       python3-pandas \
       python3-pip \
       python3-sqlalchemy \
    && apt-get clean \
    && pip3 install samtools-metrics-sqlite/ \
    && apt-get remove --purge -y \
       binutils \
       binutils-common \
       cpp \
       dpkg-dev \
       fakeroot \
       fonts-dejavu-core \
       g++ \
       gcc \
       libncurses-dev \
       libnsl-dev \
       libopenblas-dev \
       libopenblas-pthread-dev \
       libstdc++-11-dev \
       libz3-dev \
       linux-libc-dev \
       llvm-11 \
       llvm-11-dev \
       python3-pip \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
