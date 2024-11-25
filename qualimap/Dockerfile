FROM ubuntu:xenial-20210804

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG version=build-21-09-23

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       ca-certificates \
       r-base-core \
       software-properties-common \
       wget \
    && add-apt-repository ppa:justinludwig/tzdata \
    && apt-get update \
    && wget http://security.ubuntu.com/ubuntu/pool/main/o/openjdk-7/openjdk-7-jre-headless_7u211-2.6.17-0ubuntu0.1_amd64.deb \
    && apt-get install -y ./openjdk-7-jre-headless_7u211-2.6.17-0ubuntu0.1_amd64.deb \
    && rm -f ./openjdk-7-jre-headless_7u211-2.6.17-0ubuntu0.1_amd64.deb \
    && apt-get clean \
    && wget https://bitbucket.org/kokonech/qualimap/downloads/qualimap-$version.tar.gz \
    && tar xf qualimap-$version.tar.gz \
    && rm qualimap-$version.tar.gz \
    && mv qualimap-$version qualimap \
    && mv qualimap /usr/local/ \
    && apt-get remove --purge -y \
       software-properties-common \
       wget \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
