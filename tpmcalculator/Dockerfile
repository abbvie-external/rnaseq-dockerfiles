FROM ubuntu:jammy-20221130

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ENV CPPFLAGS="-I /usr/local/include/bamtools"
ENV LDFLAGS="-L /usr/local/lib/bamtools -Wl,-rpath,/usr/local/lib/bamtools"

RUN apt-get update \
        && export DEBIAN_FRONTEND=noninteractive \
        && apt-get dist-upgrade -y \
        && apt-get install -y \
           build-essential \
           cmake \
           gcc \
           g++ \
           git \
           libjsoncpp-dev \
           libjsoncpp25 \
           perl \
           make \
           software-properties-common \
           wget \
           zlib1g \
           zlib1g-dev \
        && git clone https://github.com/ncbi/TPMCalculator \
        && git clone https://github.com/pezmaster31/bamtools \
        && cd bamtools/ \
        && mkdir build \
        && cd build/ \
        && cmake ../ \
        && make \
        && make install \
        && cd / \
        && rm -rf bamtools \
        && cd TPMCalculator \
        && make \
        && mv bin/TPMCalculator /usr/local/bin \
        && cd / \
        && rm -rf TPMCalculator \
        && apt-get remove --purge -y \
           build-essential \
           cmake \
           gcc \
           g++ \
           git \
           libjsoncpp-dev \
           make \
           wget \
           zlib1g-dev \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
        && apt-get autoclean \
        && apt-get autoremove -y \
        && rm -rf /var/lib/{apt,dpkg,cache,log}/
