FROM ubuntu:oracular-20240811.1

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG version=3.2.0

RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y \
       openjdk-17-jre-headless \
       r-base \
       wget \
    && wget https://github.com/broadinstitute/picard/releases/download/$version/picard.jar \
    && mv picard.jar /usr/local/bin/ \
    && apt-get clean \
    && apt-get remove -y --purge \
       wget \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
