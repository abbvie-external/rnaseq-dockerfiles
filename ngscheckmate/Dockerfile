FROM ubuntu:jammy-20231211.1

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG bcfversion=1.19
ARG samversion=1.19
ARG NCM_HOME=/usr/local/NGSCheckMate

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        bzip2 \
        gcc \
        git \
        libbz2-1.0 \
        libbz2-dev \
        liblzma-dev \
        liblzma5 \
        libncurses6 \
        libncurses-dev \
        make \
        pkg-config \
        python2 \
        r-base-core \
        wget \
        zlib1g \
        zlib1g-dev \
    && apt-get clean \
    && wget https://github.com/samtools/bcftools/releases/download/$bcfversion/bcftools-$bcfversion.tar.bz2 \
    && wget https://github.com/samtools/samtools/releases/download/$samversion/samtools-$samversion.tar.bz2 \
    && tar xf bcftools-$bcfversion.tar.bz2 \
    && cd bcftools-$bcfversion/htslib-$bcfversion \
    && ./configure --prefix=/usr/local \
    && make \
    && make install \
    && cd ../ \
    && ./configure --prefix=/usr/local \
    && make \
    && make install \
    && cd ../ \
    && rm -rf bcftools-$bcfversion bcftools-$bcfversion.tar.bz2 \
    && tar xf samtools-$samversion.tar.bz2 \
    && cd samtools-$samversion \
    && ./configure --prefix=/usr/local \
    && make \
    && make install \
    && cd - \
    && rm -rf samtools-$samversion* \
    && cd /usr/local/ \
    && git clone https://github.com/parklab/NGSCheckMate.git \
    && sed -i 's/CFLAGS = -c/CFLAGS = -fcommon -c/' NGSCheckMate/ngscheckmate_fastq-source/Makefile \
    && cd NGSCheckMate \
    && ./install_ncmfastq.sh \
    && cd / \
    && apt-get remove --purge -y \
        build-essential \
        bzip2 \
        gcc \
        git \
        libbz2-dev \
        liblzma-dev \
        pkg-config \
        python3-dev \
        wget \
        zlib1g-dev \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
