FROM ubuntu:eoan-20200114

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \ 
       gcc \
       gfortran \
       g++ \
       libgomp1 \
       libblas-dev \
       libblas3 \
       libncurses6 \
       libncurses-dev \
       make \
       r-base-core \
       wget \
       zlib1g \
       zlib1g-dev \
    && apt-get clean \
    && Rscript -e 'install.packages(c("gtools", "gdtaa", "caTools", "KernSmooth", "gplots"));' \
    && wget --no-check-certificate https://github.com/deweylab/RSEM/archive/v1.2.25.tar.gz \
    && tar xf v1.2.25.tar.gz \
    && rm v1.2.25.tar.gz \
    && cd RSEM-1.2.25 \
    && sed -i 's/$(CC) -Wall -O2 -c -I. parseIt.cpp/$(CC) -std=c++03 -Wall -O2 -c -I. parseIt.cpp/g' Makefile \
    && sed -i 's/-g -Wall -O2/-g -Wall -std=c++03 -O2/g' sam/Makefile \
    && sed -i 's/-O3 buildReadIndex.cpp/-O3 -std=c++03 buildReadIndex.cpp/g' Makefile \
    && sed -i 's/-Wall -O3 -ffast-math/-Wall -std=c++03 -O3 -ffast-math/g' Makefile \
    && make ebseq \
    && make \
    && mv \
        convert-sam-for-rsem \
        extract-transcript-to-gene-map-from-trinity \
        rsem-bam2readdepth \
        rsem-bam2wig \
        rsem-build-read-index \
        rsem-calculate-credibility-intervals \
        rsem-calculate-expression \
        rsem-control-fdr \
        rsem-extract-reference-transcripts \
        rsem-gen-transcript-plots \
        rsem-generate-data-matrix \
        rsem-generate-ngvector \
        rsem-get-unique \
        rsem-parse-alignments \
        rsem-plot-model \
        rsem-plot-transcript-wiggles \
        rsem-prepare-reference \
        rsem-preref \
        rsem-run-ebseq \
        rsem-run-em \
        rsem-run-gibbs \
        rsem-sam-validator \
        rsem-scan-for-paired-end-reads \
        rsem-simulate-reads \
        rsem-synthesis-reference-transcripts \
        rsem-tbam2gbam \
        rsem_perl_utils.pm \
        EBSeq/rsem-for-ebseq-calculate-clustering-info \
        EBSeq/rsem-for-ebseq-find-DE \
        EBSeq/rsem-for-ebseq-generate-ngvector-from-clustering-info \
        /usr/local/bin/ \
    && cd ../ \
    && rm -rf RSEM-1.2.25 \
    && apt-get remove --purge -y \
       gcc \
       gfortran \
       g++ \
       libblas-dev \
       libncurses-dev \
       make \
       wget \
       zlib1g-dev \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
