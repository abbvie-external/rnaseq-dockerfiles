FROM oraclelinux:8.10

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG version=4.2.7-2.el8

COPY bcl-convert-$version.x86_64.rpm /

RUN dnf update -y \
    && dnf install /bcl-convert-$version.x86_64.rpm -y \
    && dnf clean all \
    && rm /bcl-convert-$version.x86_64.rpm \
    && rm -rf /tmp/* /var/tmp/*

VOLUME /var/log/bcl-convert
