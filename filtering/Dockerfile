FROM ubuntu:mantic-20240216

MAINTAINER Jeremiah Savage <jeremiah.savage@abbvie.com>

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \ 
       curl \
       gcc \
       g++ \
       gfortran \
       libblas3 \
       libblas-dev \
       liblapack3 \
       liblapack-dev \
       libcairo2 \
       libcairo2-dev \
       libcurl4 \
       libcurl4-openssl-dev \
       libfontconfig1 \
       libfontconfig-dev \
       libjpeg-turbo8 \
       libjpeg-turbo8-dev \
       libpng16-16 \
       libpng-dev \
       libssl3 \
       libssl-dev \
       libxml2-dev \
       make \
       pkg-config \
       r-base-core \
       r-base-dev \
       r-bioc-biomart \
       r-bioc-dropletutils \
       r-bioc-edger \
       r-bioc-limma \
       r-bioc-scater \
       r-bioc-singlecellexperiment \
       r-bioc-singler \
       r-cran-acepack \
       r-cran-argparse \
       r-cran-ggplot2 \
       r-cran-ggpubr \
       r-cran-jpeg \
       r-cran-latticeextra \
       r-cran-openxlsx \
       r-cran-patchwork \
       r-cran-rcpparmadillo \
       r-cran-seurat \
       r-cran-stringr \
       r-cran-svglite \
       r-cran-writexl \
       wget \
       zlib1g \
       zlib1g-dev \
    && Rscript -e 'install.packages("BiocManager"); \
        BiocManager::install(update = TRUE, ask = FALSE); \
        BiocManager::install(c("SingleCellExperiment"), update=TRUE, ask=FALSE);' \
    && apt-get clean \
    && apt-get remove --purge -y \
       curl \
       gcc \
       g++ \
       gfortran \
       libblas-dev \
       liblapack-dev \
       libcairo2-dev \
       libcurl4-openssl-dev \
       libfontconfig-dev \
       libpng-dev \
       libjpeg-turbo8-dev \
       libssl-dev \
       libxml2-dev \
       make \
       r-base-dev \
       wget \
       zlib1g-dev \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


