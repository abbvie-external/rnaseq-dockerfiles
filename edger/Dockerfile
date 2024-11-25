FROM ubuntu:noble-20240605

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

COPY edgeRKallistoScaledCounts.r /usr/local/bin/

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \ 
        gcc \
        g++ \
        gfortran \
        libhdf5-dev \
        libhdf5-103-1t64 \
        liblapack-dev \
        liblapack3 \
        make \
        r-base-core \
        r-cran-argparse \
        wget \
        zlib1g \
        zlib1g-dev \
    && Rscript -e 'install.packages("BiocManager"); \
        BiocManager::install(update = TRUE, ask = FALSE); \
        BiocManager::install(c("edgeR", "rhdf5"));' \
    && apt-get clean \
    && apt-get remove --purge -y \
        gcc \
        g++ \
        libhdf5-dev \
        liblapack-dev \
        make \
        wget \
        zlib1g-dev \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
