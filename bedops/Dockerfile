FROM fedora:40

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG version=2.4.41

RUN dnf upgrade -y \
    && dnf install -y \
       bzip2 \
       gcc \
       gcc-c++ \
       glibc-static \
       libstdc++-static \ 
       make \
       wget \
    && wget https://github.com/bedops/bedops/archive/v$version.tar.gz \
    && tar xf v$version.tar.gz \
    && rm v$version.tar.gz \
    && cd bedops-$version/ \
    && make \
    && make install \
    && mv bin/* /usr/local/bin/ \
    && cd ../ \
    && dnf remove -y \
        bzip2 \
        gcc \
        gcc-c++ \
        glibc-static \
        libstdc++-static \
        make \
        wget \
    && rm -rf bedops-$version
