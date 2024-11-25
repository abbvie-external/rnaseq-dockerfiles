FROM ubuntu:noble-20240827.1

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

COPY rnaseq-scripts/* /usr/local/bin/

RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get upgrade --no-install-recommends -y \
    && apt-get install --no-install-recommends -y \
        python3 \
        python3-pandas \
        python3-pysam \
        python3-ruamel.yaml \
    && apt-get clean \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
