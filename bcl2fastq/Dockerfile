FROM ubuntu:groovy-20210115

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG version=2.20.0.422

COPY bcl2fastq2-v$version-Source.tar.gz /

RUN apt-get update \
        && export DEBIAN_FRONTEND=noninteractive \
        && apt-get dist-upgrade -y \
        && apt-get install -y \
           build-essential \
           gcc \
           g++ \
           libpthread-stubs0-dev \
           zlib1g \
           zlib1g-dev \
        && export TMP=/tmp \
        && export SOURCE=${TMP}/bcl2fastq \
        && export BUILD=${TMP}/bcl2fastq2-v$version-build \
        && export INSTALL_DIR=/usr/local \
        && export C_INCLUDE_PATH=/usr/include/x86_64-linux-gnu \
        && cd ${TMP} \
        && tar xvf /bcl2fastq2-v$version-Source.tar.gz \
        && mkdir ${BUILD} \
        && cd ${BUILD} \
        && ${SOURCE}/src/configure --prefix=${INSTALL_DIR} \
        && make \
        && make install \
        && cd / \
        && rm -f /bcl2fastq2-v$version-Source.tar.gz \
        && apt-get remove --purge -y \
           build-essential \
           gcc \
           g++ \
           libpthread-stubs0-dev \
           zlib1g-dev \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
        && apt-get autoclean \
        && apt-get autoremove -y \
        && rm -rf /var/lib/{apt,dpkg,cache,log}/
