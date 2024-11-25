FROM fedora:31

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

COPY tar-concat /tar-concat/

RUN dnf upgrade -y \
    && dnf install -y \
       python3-pip \
    && pip3 install tar-concat/ \
    && dnf clean all
