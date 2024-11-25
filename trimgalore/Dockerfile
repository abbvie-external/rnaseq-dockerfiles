FROM ubuntu:jammy-20221130

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG tgversion=0.6.7
ARG fqversion=v0.11.9

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \ 
        openjdk-19-jre-headless \
        perl-modules \
        pigz \
        python3-minimal \
        python3-pip \
        unzip \
        wget \
    && apt-get clean \
    && wget --no-check-certificate https://github.com/FelixKrueger/TrimGalore/archive/$tgversion.tar.gz \
    && wget --no-check-certificate http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_$fqversion.zip \
    && tar xf $tgversion.tar.gz \
    && mv TrimGalore-$tgversion/trim_galore /usr/local/bin/ \
    && rm -rf $tgversion.tar.gz TrimGalore-$tgversion \
    && pip3 install cutadapt \
    && unzip fastqc_$fqversion.zip \
    && rm *.zip \
    && mv FastQC /usr/local/ \
    && chmod 755 /usr/local/FastQC/fastqc \
    && sed -i 's/kmer[[:space:]]\+ignore[[:space:]]\+1/kmer ignore 0/' /usr/local/FastQC/Configuration/limits.txt \
    && apt-get remove --purge -y \
        python3-pip \
        unzip \
        wget \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
