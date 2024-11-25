FROM ubuntu:focal-20240530

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG version=2.7.4

RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get dist-upgrade -y \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       gcc \
       g++ \
       libcurl4 \
       libcurl4-openssl-dev \
       libssl1.1 \
       libssl-dev \
       make \
       python3-dev \
       python3-pip \
       python3-venv \
       ruby \
       ruby-dev \
       ruby-public-suffix \
       zlib1g-dev \
    && apt-get clean \
    && gem install arvados-cli -v $version \
    && python3 -m venv .venv \
    && . .venv/bin/activate \
    && pip install arvados-python-client==$version \
    && apt-get remove --purge -y \
       gcc \
       g++ \
       libcurl4-openssl-dev \
       libssl-dev \
       make \
       python3-dev \
       ruby-dev \
       zlib1g-dev \
    && apt-get autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
