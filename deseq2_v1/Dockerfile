FROM ubuntu:eoan-20200114

MAINTAINER Claire Chai <yating.chai@abbvie.com>

COPY cpm.DEseq2.degenes.R . 
RUN chmod 755 /cpm.DEseq2.degenes.R

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \ 
        gcc \
        g++ \
	gfortran \
        make \
        r-base-core \
        wget \
        zlib1g \
        zlib1g-dev \
	curl \
	libcurl4-openssl-dev libxml2-dev pkg-config \
	libblas-dev liblapack-dev libpng-dev \
	r-cran-rcpparmadillo r-cran-acepack r-cran-latticeextra r-cran-jpeg \

    && Rscript -e 'install.packages("BiocManager"); \
        BiocManager::install(update = TRUE, ask = FALSE); \
        BiocManager::install(c("DESeq2"));' \
    && apt-get clean \
    && apt-get remove --purge -y \
        gcc \
        g++ \
        make \
        wget \
        zlib1g-dev \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*



