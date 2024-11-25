FROM ubuntu:jammy-20221130

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \ 
       ca-certificates \
       curl \
       perl \
    && sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)" \
    && mv /root/edirect/* /usr/local/bin/ \
    && apt-get clean \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
