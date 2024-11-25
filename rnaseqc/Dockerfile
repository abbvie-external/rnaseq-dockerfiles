FROM ubuntu:noble-20240605

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG version=2.4.2

RUN apt-get update \
        && export DEBIAN_FRONTEND=noninteractive \
        && apt-get dist-upgrade -y \
        && apt-get install -y \
           autotools-dev \
           build-essential \
           cmake \
           git \
           libhts3t64 \
           libhts-dev \
           python3 \
           python3-matplotlib \
           python3-nbformat \
           python3-numpy \
           python3-pandas \
           python3-pip \
           python3-pybigwig \
           python3-scipy \
           python3-seaborn \
           python3-setuptools \
           libboost-filesystem-dev \
           libboost-regex-dev \
           python3-sklearn \
           libboost-system-dev \
           libbz2-1.0 \
           libbz2-dev \
           libcurl4 \
           libcurl4-gnutls-dev \
           liblzma5 \
           liblzma-dev \
           libpthread-stubs0-dev \
           software-properties-common \
           wget \
           zlib1g \
           zlib1g-dev \
        && pip3 install agutil bx-python --break-system-packages \
        && wget https://github.com/broadinstitute/rnaseqc/archive/v$version.tar.gz \
        && tar xf v$version.tar.gz \
        && cd rnaseqc-$version \
        && git clone --recursive https://github.com/walaj/SeqLib.git \
        && git clone https://github.com/francois-a/rnaseq-utils \
        && cd SeqLib \
        && sed -i 's/const uint8_t rle_auxtab/extern const uint8_t rle_auxtab/g' bwa/rle.h \
        && sed -i 's/const uint8_t rle_auxtab/extern const uint8_t rle_auxtab/g' fermi-lite/rle.h \
        && mkdir build \
        && cd build
        # && cmake .. \
        # && make \
        # && make install \
        # && cd ../ \
        # && make \
        # && mv rnaseqc /usr/local/bin/ \
        # && cd rnaseq-utils/ \
        # && mv annotation.py rnaseqnorm.py /usr/local/bin/ \
        # && cd / \
        # && rm v$version.tar.gz \
        # && rm -rf rnaseqc-$version \
        # && mkdir -p /root/.config/matplotlib \
        # && echo "backend	:	Agg" > /root/.config/matplotlib/matplotlibrc \
        # && cd /usr/local/bin/ \
        # && wget https://raw.githubusercontent.com/broadinstitute/gtex-pipeline/master/gene_model/collapse_annotation.py \
        # && chmod +x collapse_annotation.py \
        # && cd / \
        # && apt-get remove --purge -y \
        #    autotools-dev \
        #    build-essential \
        #    cmake \
        #    git \
        #    libbz2-dev \
        #    libcurl4-gnutls-dev \
        #    libhts-dev \
        #    liblzma-dev \
        #    libpthread-stubs0-dev \
        #    python3-pip \
        #    python3-setuptools \
        #    software-properties-common \
        #    wget \
        #    zlib1g-dev \
        # && apt-get clean \
        # && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
        # && apt-get autoclean \
        # && apt-get autoremove -y --purge \
        # && rm -rf /var/lib/{apt,dpkg,cache,log}/

ENV PYTHONPATH $PYTHONPATH:/usr/local/bin/
