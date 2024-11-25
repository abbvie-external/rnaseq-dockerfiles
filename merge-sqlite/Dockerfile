FROM fedora:40

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

COPY merge-sqlite/ /merge-sqlite/

RUN dnf upgrade -y --setopt=install_weak_deps=False \
    && dnf install -y --setopt=install_weak_deps=False \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        sqlite \
        zlib \
        zlib-devel \
    && cd merge-sqlite/ \
    && pip wheel . \
    && pip install merge_sqlite-0.1-py2.py3-none-any.whl \
    && cd ../ \
    && rm -rf merge-sqlite \
    && dnf remove -y \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        zlib-devel \
    && dnf clean all \
    && rm -rf /tmp/* /var/tmp/*
