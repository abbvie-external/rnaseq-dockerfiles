FROM ubuntu:noble-20240605

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG version=0.51.0

RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get dist-upgrade -y \
    && apt-get install -y --no-install-recommends\
        autoconf \
        automake \
        ca-certificates \
        cmake \
        gcc \
        g++ \
        libhdf5-cpp-103-1t64 \
        libhdf5-dev \
        libhdf5-fortran-102t64 \
        libhdf5-hl-fortran-100t64 \
        make \
        wget \
    && apt-get clean \
    && wget --no-check-certificate https://github.com/pachterlab/kallisto/archive/v$version.tar.gz \
    && tar xf v$version.tar.gz \
    && cd kallisto-$version/ext/htslib \
    && sed '/AC_PROG_CC/a AC_CANONICAL_HOST AC_PROG_INSTALL' configure.ac > configure.ac2 \
    && mv configure.ac2 configure.ac \
    && autoreconf -i \
    && autoheader \
    && autoconf \
    && cd ../../ \
    && mkdir build \
    && cd build \
    && cmake .. -DZLIBNG=ON -DUSE_BAM=ON -DBUILD_FUNCTESTING=ON -DUSE_HDF5=ON \
    && make \
    && make install \
    && cd ../../ \
    && rm -rf kallisto* v$version.tar.gz \
    && apt-get remove --purge -y \
        autoconf \
        automake \
        ca-certificates \
        cmake \
        gcc \
        g++ \
        libhdf5-dev \
        make \
        wget \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
