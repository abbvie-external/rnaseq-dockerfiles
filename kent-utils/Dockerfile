FROM fedora:40

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG version=443_preview2
ARG machtype=x86_64

RUN dnf upgrade -y \
    && dnf install -y \
        gcc \
        gcc-c++ \
        hostname \
        libpng \
        libpng-devel \
        libuuid \
        libuuid-devel \
        make \
        mariadb-connector-c \
        mariadb-devel \
        patch \
        perl \
        perl-Getopt-Long \
        python2 \
        wget \
    && wget https://github.com/ucscGenomeBrowser/kent/archive/refs/tags/v$version.tar.gz \
    && tar xf v$version.tar.gz \
    && rm v$version.tar.gz \
    && cd kent-$version/ \
    && export MACHTYPE=$machtype \
    && mkdir -p ~/bin/$machtype \
    && mkdir -p /usr/local/apache/cgi-bin \
    && cd src/lib/ \
    && make \
    && cd ../jkOwnLib/ \
    && make \
    && cd ../htslib/ \
    && make \
    && cd ../optimalLeaf \
    && make \
    && cd ../hg/ \
    && make compile \
    && cd ../utils/ \
    && make \
    && cd ../hg/utils/ \
    && make \
    && cd / \
    && rm -rf kent-$version \
    && mv /root/bin/$machtype/* /usr/local/bin/ \
    && mv /root/bin/scripts/* /usr/local/bin/ \
    && rm -rf /root/bin \
    && dnf remove -y \
        gcc \
        gcc-c++ \
        hostname \
        libpng-devel \
        libuuid-devel \
        make \
        mariadb-devel \
        patch \
        unzip \
        wget \
    && dnf clean all \
    && rm -rf /tmp/* /var/tmp/*
