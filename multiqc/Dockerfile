FROM ubuntu:oracular-20240913

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG version=1.19

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       python3-pip \
       zlib1g \
    && apt-get clean \
    && pip install multiqc==$version --break-system-packages --root-user-action=ignore \
    && pip cache purge \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
